import time
import tkinter
from selenium import webdriver
import  pandas as pd;
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pathlib import Path
from configparser import ConfigParser
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


class WhatsApp():
    def __init__(self):
        self.link='https://wa.me/'
        self.driver='';
        self.cfg = ConfigParser()
        self.cfg.read('config.ini')
        self.config_path=self.cfg.get("info",'config_path')
        self.userprofile=self.cfg.get("info","userprofile")
        self.buildGui()


    def start_driver(self,config_path,profil_path):
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir="+config_path);
        options.add_argument("profile-directory="+profil_path);
        self.driver = webdriver.Chrome(options=options);
        self.driver.get("https://web.whatsapp.com/")

    def prepare_numbers(self,numbers_path):
        df=pd.read_excel(numbers_path);
        newList=[]
        for index, row in df.iterrows():
            tmp=str(row['Phone']);
            tmp=tmp.replace(' ','');
            tmp=tmp.replace('-','');
            tmp=tmp.replace('+','');
            if tmp[0]=='0':
                tmp=tmp[1:]
                tmp='212'+tmp;

            tmp=self.link+tmp
            newList.append(tmp)
        return newList;
    def read_msg(self ,msg_path):
        with open(msg_path) as f:
            contents = f.read()
        return contents;
    def sendImgOrVideo(self,list_img):
        msg_img=self.read_msg(list_img)
        WebDriverWait(self.driver, 120).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div._2jitM")));
        attchementButt=self.driver.find_element(By.CSS_SELECTOR,'div._2jitM');
        time.sleep(2)
        attchementButt.click()
        time.sleep(2)
        WebDriverWait(self.driver, 120).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._2t8DP")));
        time.sleep(2)
        photo_button=self.driver.find_element(By.CSS_SELECTOR,'button._2t8DP');
        time.sleep(2)
        input_imgs=photo_button.find_element(By.TAG_NAME,'input')
        input_imgs.send_keys(msg_img)
        time.sleep(2)
        send1_key = self.driver.find_element(By.CSS_SELECTOR, 'div._165_h._2HL9j');
        time.sleep(2)
        send1_key.click();


    def sendMegs(self,numbers_path,msg_path,list_img):

        list_of_phones= self.prepare_numbers(numbers_path);
        msg=self.read_msg(msg_path)
        self.start_driver(self.config_path,self.userprofile)
        for number in list_of_phones:
            try:
                time.sleep(30)
                self.driver.get(number)
                time.sleep(2)
                continue_btn = self.driver.find_element(By.ID, 'action-button');
                time.sleep(2)
                continue_btn.click()
                time.sleep(2)
                us_browser_btn = self.driver.find_element(By.LINK_TEXT, 'use WhatsApp Web');
                time.sleep(2)
                us_browser_btn.click()
                time.sleep(2)
                WebDriverWait(self.driver, 120).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div._13NKt.copyable-text.selectable-text")));
                time.sleep(2)
                text_field = self.driver.find_elements(By.CSS_SELECTOR, 'div._13NKt.copyable-text.selectable-text')[1];
                time.sleep(2)
                text_field.click()
                time.sleep(2)
                text_field.send_keys(msg);
                time.sleep(2)
                send_key = self.driver.find_element(By.CSS_SELECTOR, 'button.tvf2evcx.oq44ahr5.lb5m6g5c.svlsagor.p2rjqpw5.epia9gcq');
                time.sleep(2)
                send_key.click();
                time.sleep(5)
                self.sendImgOrVideo(list_img)
            except Exception as e:
                print(e)


        print('Done!')

    def buildGui(self):

        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path("./assets")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        window = Tk()
        config_path=tkinter.StringVar();
        profil_path=tkinter.StringVar();
        numbers_path=tkinter.StringVar();
        msg_path=tkinter.StringVar();
        images_path=tkinter.StringVar();
        window.geometry("830x564")
        window.configure(bg="#FFFFFF")

        canvas = Canvas(
            window,
            bg="#FFFFFF",
            height=664,
            width=830,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0,
            0.0,
            830.0,
            664.0,
            fill="#FFFFFF",
            outline="")



        canvas.create_text(
            201.0,
            21.0,
            anchor="nw",
            text="WHATTSAPP BOT",
            fill="#06C776",
            font=("Poppins Bold", 48 * -1)
        )

        # entry_image_1 = PhotoImage(
        #     file=relative_to_assets("entry_1.png"))
        # entry_bg_1 = canvas.create_image(
        #     414.5,
        #     185.5,
        #     image=entry_image_1
        # )
        # entry_1 = Entry(
        #     bd=0,
        #     bg="#DBDBDB",
        #     highlightthickness=0,
        #     textvariable=config_path
        # )
        # entry_1.place(
        #     x=154.5,
        #     y=160.0,
        #     width=520.0,
        #     height=49.0
        # )
        # canvas.create_text(
        #     279.0,
        #     135.0,
        #     anchor="nw",
        #     text="configuration path",
        #     fill="#000000",
        #     font=("Noto Sans", 16 * -1)
        # )
        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.sendMegs(numbers_path.get(),msg_path.get(),images_path.get()),
            relief="flat"
        )
        button_2.place(
            x=349.0,
            y=500.0,
            width=102.0,
            height=30.75
        )

        entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        entry_bg_3 = canvas.create_image(
            414.5,
            205.5,
            image=entry_image_3
        )
        entry_3 = Entry(
            bd=0,
            bg="#DBDBDB",
            highlightthickness=0,
            textvariable=numbers_path,
        )
        entry_3.place(
            x=154.5,
            y=180.0,
            width=520.0,
            height=49.0
        )

        canvas.create_text(
            370.0,
            150.0,
            anchor="nw",
            text="Numbers  Path",
            fill="#000000",
            font=("Noto Sans", 16 * -1)
        )

        entry_image_4 = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        entry_bg_4 = canvas.create_image(
            414.5,
            328.5,
            image=entry_image_4
        )
        entry_4 = Entry(
            bd=0,
            bg="#DBDBDB",
            highlightthickness=0,
            textvariable=msg_path
        )
        entry_4.place(
            x=154.5,
            y=305.0,

            width=520.0,
            height=49.0
        )

        canvas.create_text(
            370.0,
            270.0,
            anchor="nw",
            text="Message path",
            fill="#000000",
            font=("Noto Sans", 16 * -1)
        )
        #----------------------------------------------------------
        entry_image_5 = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        entry_bg_4 = canvas.create_image(
            414.5,
            455.5,
            image=entry_image_4
        )
        entry_5 = Entry(
            bd=0,
            bg="#DBDBDB",
            highlightthickness=0,
            textvariable=images_path
        )
        entry_5.place(
            x=154.5,
            y=430.0,

            width=520.0,
            height=49.0
        )

        canvas.create_text(
            370.0,
            380.0,
            anchor="nw",
            text="Images path",
            fill="#000000",
            font=("Noto Sans", 16 * -1)
        )
        #--------------------------------------------------------

        canvas.create_text(
            646.0,
            500.0,
            anchor="nw",
            text="sswaad06@gmail.com",
            fill="#000000",
            font=("Noto Sans", 16 * -1)
        )




        window.resizable(False, False)
        window.mainloop()


if __name__ == '__main__':
    op= WhatsApp()