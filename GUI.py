import wx
import requests
import json
import cv2
from PIL import Image
import numpy as np

class WeatherApp(wx.Frame):
    def __init__(self, parent, title):
        super(WeatherApp, self).__init__(parent, title=title, size=(1228, 816))

        font = wx.Font(19, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, 'Arial')
        font2 = wx.Font(25, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, 'Arial')
        font3 = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, 'Arial')

        bmp = wx.Bitmap("/Users/anshumaansoni/Downloads/ruslan-sikunov-1GnIsmo48bM-unsplash.jpg",wx.BITMAP_TYPE_ANY)
        img = bmp.ConvertToImage()
        img = img.Scale(1228,816, wx.IMAGE_QUALITY_HIGH)
        bmp = wx.Bitmap(img)
        self.Background_bitmap = wx.StaticBitmap(self, -1, bmp)

        panel = wx.Panel(self)
        city_label = wx.StaticText(panel, label="City:")
        self.city_text = wx.TextCtrl(panel, size=(300,-1))
        get_weather_button = wx.Button(panel, label="Get Weather")

        self.city_text.SetFont(font2)
        city_label.SetFont(font3)
        get_weather_button.SetFont(font)

        get_weather_button.Bind(wx.EVT_BUTTON, self.get_weather)

        sizer = wx.GridBagSizer(0,0)
        sizer.Add(city_label, (0, 0))
        sizer.Add(self.city_text, (1, 0), flag=wx.EXPAND)
        sizer.Add(get_weather_button, (1, 1), flag=wx.EXPAND)
        panel.SetSizerAndFit(sizer)

        self.Centre()
        self.Show()

    def encode_image(self, img):
        success, encoded_image = cv2.imencode('.png', img)
        return encoded_image

    def decode_image_to_wxBitmap(self, encoded_image):
        img = cv2.imdecode(encoded_image, cv2.IMREAD_UNCHANGED)
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        wx_bitmap = wx.Bitmap.FromBuffer(img_pil.size[0], img_pil.size[1], img_pil.tobytes())
        return wx_bitmap

    def text_to_image(self, text, text2, path, org, org2, color, resize, scale1, scale2):
        img_pil= cv2.imread(path)
        img_pil=cv2.cvtColor(img_pil, cv2.COLOR_BGR2RGB)
        img_pil= cv2.resize(img_pil, resize)
        k=np.ones((8,8))
        cv2.putText(img_pil,text, org=org ,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=scale1, color=color, thickness=6)
        cv2.putText(img_pil, text2, org=org2, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=scale2, color=color, thickness=15 )
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGBA2BGRA)
        return img_cv

    def textimage(self, text, text2, path, org, org2, color, resize, scale1, scale2):
        img = self.text_to_image(text, text2, path, org, org2, color, resize, scale1, scale2)
        encoded_img = self.encode_image(img)
        bitmap = self.decode_image_to_wxBitmap(encoded_img)
        return bitmap

    def get_weather(self, event):
        city = self.city_text.GetValue()
        api_key = "18a656c2bab7188174d73f2d0900357b"  # Replace with your OpenWeatherMap API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = json.loads(response.text)

            temp = data['main']['temp']
            temp = round(temp)
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            weather_desc = data['weather'][0]['description']

            bmp2 = self.textimage("Humidity",f"{humidity}%", "/Users/anshumaansoni/Downloads/randy-laybourne-Y9awChpvLRo-unsplash.jpg",
                                  (400, 300), (440,470), color=(255,255,255), resize=(1228,816), scale1=2, scale2=7)
            img = bmp2.ConvertToImage()
            img = img.Scale(614, 408, wx.IMAGE_QUALITY_HIGH)
            self.Background_bitmap2 = wx.StaticBitmap(self, -1, img, (614, 408))

            bmp2 = self.textimage("Temp",f'{str(temp)} C', "/Users/anshumaansoni/Downloads/michael-behrens-48qa_84IvPY-unsplash.jpg",
                                  (380, 320), (360,500), color=(255,255,255), resize=(1228,816), scale1=2, scale2=7)
            img = bmp2.ConvertToImage()
            img = img.Scale(614, 408, wx.IMAGE_QUALITY_HIGH)
            self.Background_bitmap2 = wx.StaticBitmap(self, -1, img, (0, 408))

            bmp2 = self.textimage("Wind",f"{str(wind_speed)} m/s", "/Users/anshumaansoni/Downloads/jason-mavrommatis-9HEY1URQIQY-unsplash.jpg",
                                  (240, 300), (200,470), color=(90,90,90), resize=(1228,816), scale1=2, scale2=6)
            img = bmp2.ConvertToImage()
            img = img.Scale(614, 408, wx.IMAGE_QUALITY_HIGH)
            self.Background_bitmap2 = wx.StaticBitmap(self, -1, img, (614, 0))

            if len(weather_desc.split())>1:
                a,b=weather_desc.split()
                bmp2 = self.textimage(a, b,
                                      "/Users/anshumaansoni/Downloads/weatherimage.jpg",
                                      (220, 290), (230, 380), color=(255, 255, 255), resize=(1228, 656), scale1=6, scale2=4)
                img = bmp2.ConvertToImage()
                img = img.Scale(614, 328, wx.IMAGE_QUALITY_HIGH)
                self.Background_bitmap2 = wx.StaticBitmap(self, -1, img, (0, 80))

            else:
                bmp2 = self.textimage("", weather_desc,
                                      "/Users/anshumaansoni/Downloads/weatherimage.jpg",
                                      (110, 130), (260, 380), color=(255, 255, 255), resize=(1228, 656), scale1=1, scale2=7)
                img = bmp2.ConvertToImage()
                img = img.Scale(614, 328, wx.IMAGE_QUALITY_HIGH)
                self.Background_bitmap2 = wx.StaticBitmap(self, -1, img, (0, 80))



        except Exception as e:
            wx.MessageBox("Error fetching weather data.",f'Error{e}', wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    WeatherApp(None, title="Weather App")
    app.MainLoop()
