from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64


@login_required
def two_factor_setup(request):
    """
    Setup 2FA for the user
    """
    # Check if user already has 2FA devices
    devices = list(devices_for_user(request.user))
    if devices:
        messages.info(request, 'You already have 2FA enabled.')
        return redirect('two_factor_dashboard')

    # Create TOTP device for the user
    device = TOTPDevice.objects.create(user=request.user, name='Default')

    # Generate QR code for the device
    qr_code = device.config_url

    # Create QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_code)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64 for display in template
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'qr_code': img_str,
        'secret_key': device.bin_key.hex(),
        'device': device,
    }

    return render(request, 'two_factor/setup.html', context)


@login_required
def two_factor_verify(request):
    """
    Verify 2FA token
    """
    if request.method == 'POST':
        token = request.POST.get('token')

        # Verify token against user's devices
        for device in devices_for_user(request.user):
            if device.verify_token(token):
                # Token is valid, mark device as confirmed if it's TOTP
                if isinstance(device, TOTPDevice):
                    device.confirmed = True
                    device.save()

                # Mark user as verified in session
                request.session['otp_verified'] = True

                messages.success(request, 'Two-factor authentication enabled successfully!')
                return redirect('dashboard')

        messages.error(request, 'Invalid token. Please try again.')

    return render(request, 'two_factor/verify.html')


@login_required
def two_factor_dashboard(request):
    """
    Dashboard for managing 2FA settings
    """
    devices = list(devices_for_user(request.user))

    context = {
        'devices': devices,
    }

    return render(request, 'two_factor/dashboard.html', context)


@login_required
def two_factor_disable(request, device_id):
    """
    Disable a 2FA device
    """
    try:
        device = TOTPDevice.objects.get(id=device_id, user=request.user)
        device.delete()
        messages.success(request, 'Two-factor authentication disabled for this device.')
    except TOTPDevice.DoesNotExist:
        messages.error(request, 'Device not found.')

    return redirect('two_factor_dashboard')
