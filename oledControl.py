'''
- Raspberry pi zero w와 0.96” monochrome oled display를 사용하여 시계/ 캘린더를 제작
- tact switch(모드버튼)을 사용해 시계모드와 달력모드를 전환
- 모드 버튼은 인터럽트를 사용하여 언제라도 즉각적으로 반응
'''

# 모듈 임포트
from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from datetime import datetime, timedelta, timezone
import RPi.GPIO as GPIO

# 환경 설정 및 초기화
disp_width, disp_height = 64, 128 # oled portrait layout
RST, DC, SPI_PORT, SPI_DEVICE = 24, 25, 0,0 # oled 핀설정
TimeZone = timezone(timedelta(hours =+ 9)) # 서울 표준시 사용

font_small = ImageFont.truetype('malgun.ttf', 15)
font_big = ImageFont.truetype('malgun.ttf', 25)
MODE_BUTTON = 12 # GPIO 핀 할당

# mode 초기화
mode_list = []
mode_index = 0
current_mode = None

# 모드 추상클래스
class Mode():
    def __init__(self):
        self.screenImage = Image.new('1', (disp_width, disp_height), 0) # mode '1'은 단색 비트맵이미지, 배경색 0
        self.draw = ImageDraw.Draw(self.screenImage) # PIL 드로우 핸들

    # 현재시간 확인
    def getCurrentTime(self):
        return datetime.now(TimeZone)

    # 표시할 이미지 업데이트
    def update(self):
        pass

    # 가운데 정렬하기 - 텍스트를 화면중앙에 정렬하고자 할 때 시작점 xy 리턴
    def getTextCenterAlignXY(self, text, font):
        centerX = (disp_width - self.draw.textsize(text, font = font)[0]) // 2
        centerY = (disp_height - self.draw.textsize(text, font = font)[1]) //2
        return (centerX, centerY)

# 시계모드
class ClockMode(Mode):

    # 현재시간을 확인해 표시할 이미지 만듬
    def update(self):
        # 현재시간 확인
        now = self.getCurrentTime()
        # 시계화면 구성
        self.draw.rectangle((0, 0, disp_width, disp_height), fill = 0) # 화면 지움
        self.draw.text((2, 30), now.strftime('%p'), font = font_small, fill = 1) # am/pm
        self.draw.text((0, 50), now.strftime('%I:%M'), font = font_big, fill = 1) # 시:분
        self.draw.text((40, 80), now.strftime('%S'), font = font_small, fill = 1) # :초

# 달력모드
class CalendarMode(Mode):

    # 화면 업데이트
    def update(self):
        # 현재시간 확인
        now = self.getCurrentTime()
        # 달력화면 구성
        self.draw.rectangle((0, 0, disp_width, disp_height), fill = 0) # 화면 지움
        year = str(now.year) # 년도
        self.draw.text((self.getTextCenterAlignXY(year, font_small)[0], 20), year, font = font_small, fill = 1)
        month = str(now.month) # 월
        self.draw.text((20,40), month, font = font_big, fill = 1)
        self.draw.text((20 + len(month)*13, 50), '월', font = font_small, fill = 1)
        day = str(now.day) #일
        self.draw.text((20, 65), day, font = font_big, fill = 1)
        self.draw.text((20 + len(day)*13, 75), '일', font = font_small, fill = 1)
        weekday = '월화수목금토일'[now.weekday()] # 요일
        self.draw.text((self.getTextCenterAlignXY(weekday + '요일', font_small)[0], 95), weekday + '요일', font = font_small, fill = 1)

#  버튼 초기화
def initButton():
    GPIO.setmode(GPIO.BCM)
    button = MODE_BUTTON
    GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP) # 내장 풀업 사용 (안눌렸을 때 high, 눌리면 low)
    GPIO.add_event_detect(button, GPIO.FALLING, callback = whenButtonPressed, bouncetime = 200) # 인터럽트 사용, debounce 사용

# 버튼 인터럽트 콜백함수
def whenButtonPressed(channel):
    global mode_index
    global current_mode
    global mode_list

    print(f'button {channel} pressed!')

    if channel == MODE_BUTTON:
        print(f'mode: {mode_index}')
        mode_index = 1 if mode_index == 0 else 0 # 0이었다면 1, 1이었다면 0
        current_mode = mode_list[mode_index]

# 메인
def main():
    # oled  디스플레이 초기화
    oled = Adafruit_SSD1306.SSD1306_128_64(rst = RST, dc = DC, spi = SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz = 8000000))
    oled.begin()
    oled.clear()
    oled.display()

    # mode 초기화
    global mode_list
    mode_list = [ClockMode(), CalendarMode()] # 시계모드, 달력모드
    global mode_index
    mode_index = 0
    global current_mode
    current_mode = mode_list[mode_index]

    # 버튼 초기화
    initButton()

    # 무한반복 - 키보드 인터럽트(Ctr-c)가 있으면 종료
    try:
        while True:
            # 현재 모드에 따라 업데이트 실행
            current_mode.update()
            # oled 디스플레이 업데이트
            rotatedImage = current_mode.screenImage.transpose(Image.ROTATE_90) # 화면을 90도 회전
            # FLIP_LEFT_RIGHT : 좌우 반전
            # FLIP_TOP_BOTTOM : 상하 반전
            flippedImage = rotatedImage.transpose(Image.FLIP_LEFT_RIGHT)
            oled.image(flippedImage)
            oled.display()

    except KeyboardInterrupt:
        print('사용자에 의해 실행을 중단합니다...')
        oled.clear()
        oled.display()

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()


