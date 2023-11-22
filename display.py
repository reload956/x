import digitalio
import board
import subprocess
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7735 as st7735        # pylint: disable=unused-import

class Display:

    # Configuration for CS and DC pins (these are PiTFT defaults):
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = digitalio.DigitalInOut(board.D24)

    # Config for display baudrate (default max is 24mhz):
    BAUDRATE = 24000000

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()

    def __init__(self):
        # Create the display:
        self.disp = st7735.ST7735R(self.spi, rotation=90,                           # 1.8" ST7735R
                            cs=self.cs_pin, dc=self.dc_pin, rst=self.reset_pin, baudrate=self.BAUDRATE)
        # pylint: enable=line-too-long
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if self.disp.rotation % 180 == 90:
            self.height = self.disp.width   # we swap height/width to rotate it to landscape!
            self.width = self.disp.height
        else:
            self.width = self.disp.width   # we swap height/width to rotate it to landscape!
            self.height = self.disp.height


    def draw_image(self,path):
        self.disp_clear()
        image = Image.new('RGB', (self.width, self.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.disp.image(image)

        image = Image.open(path)

        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = self.width / self.height
        if screen_ratio < image_ratio:
            scaled_width = image.width * self.height // image.height
            scaled_height = self.height
        else:
            scaled_width = self.width
            scaled_height = image.height * self.width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # Crop and center the image
        x = scaled_width // 2 - self.width // 2
        y = scaled_height // 2 - self.height // 2
        image = image.crop((x, y, x + self.width, y + self.height))

        # Display image.
        self.disp.image(image)

    def disp_clear(self):
        self.disp.clear()

    def print_text(self, text):
        self.disp_clear()
        image = Image.new('RGB', (self.width, self.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.disp.image(image)
        # First define some constants to allow easy positioning of text.
        padding = -2
        x = 0
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
        draw.text((x, padding), text, font=font, fill="#FFFFFF")

    def print_stats(self):
        self.disp_clear()
        image = Image.new('RGB', (self.width, self.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.disp.image(image)
        # First define some constants to allow easy positioning of text.
        padding = -2
        x = 0
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)

        cmd = "hostname -I | cut -d\' \' -f1"
        IP = "IP: "+subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk \'{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}\'" # pylint: disable=line-too-long
        Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

        # Write four lines of text.
        y = padding
        draw.text((x, y), IP, font=font, fill="#FFFFFF")
        y += font.getsize(IP)[1]
        draw.text((x, y), CPU, font=font, fill="#FFFF00")
        y += font.getsize(CPU)[1]
        draw.text((x, y), MemUsage, font=font, fill="#00FF00")
        y += font.getsize(MemUsage)[1]
        draw.text((x, y), Disk, font=font, fill="#0000FF")
        y += font.getsize(Disk)[1]
        draw.text((x, y), Temp, font=font, fill="#FF00FF")

        # Display image.
        self.disp.image(image)




