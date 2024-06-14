import time
from onvif import ONVIFCamera

class ThermalCamera:
    def __init__(self, ip, port, user, password, wsdl):
        self.camera = ONVIFCamera(ip, port, user, password, wsdl)
        self.media_service = self.camera.create_media_service()
        self.ptz_service = self.camera.create_ptz_service()

    def print_profile_data(self):
        profiles = self.media_service.GetProfiles()
        for profile in profiles:
            print(f"Nombre del Perfil: {profile.Name}")
            print(f"Token del Perfil: {profile.token}")
            if profile.VideoEncoderConfiguration:
                print(f"Resolución: {profile.VideoEncoderConfiguration.Resolution}")
                print(f"Frame Rate: {profile.VideoEncoderConfiguration.RateControl.FrameRateLimit}")
                print(f"Bit Rate: {profile.VideoEncoderConfiguration.RateControl.BitrateLimit}")

    def move_camera_absolute(self, profile_token, x, y, zoom):
        request = self.ptz_service.create_type('AbsoluteMove')
        request.ProfileToken = profile_token
        request.Position = {'PanTilt': {'x': x, 'y': y}, 'Zoom': {'x': zoom}}
        
        self.ptz_service.AbsoluteMove(request)
    
    def move_camera_continuous(self, profile_token, x, y, zoom_duration=2):
        request = self.ptz_service.create_type('ContinuousMove')
        request.ProfileToken = profile_token
        request.Velocity = {'PanTilt': {'x': x, 'y': y}}

        self.ptz_service.ContinuousMove(request)
        
        time.sleep(zoom_duration)
        self.ptz_service.Stop({'ProfileToken': profile_token})