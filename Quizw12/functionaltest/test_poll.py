from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mypoll.models import Poll, Choice
from django.urls import reverse
import time

class testUserPlayPoll(StaticLiveServerTestCase):
    def setUp(self):
        
        self.poll = Poll.objects.create(name="แมวหรือหมา")
        self.choice1 = Choice.objects.create(poll=self.poll, name="แมว", vote_count=1)
        self.choice2 = Choice.objects.create(poll=self.poll, name="หมา", vote_count=2)

        self.browser = webdriver.Chrome()
    def tearDown(self):
        self.browser.quit()

    def test(self):
        # ปาร์คได้ยินมาจากเพื่อนเรื่องเว็บ polls ปาร์คจึงอยากลองเล่นดู
        # ปาร์คเข้ามาที่หน้าเว็บ
        self.browser.get(self.live_server_url)
        # ปาร์คเห็นลิงิค์ poll อยู่ 1 อันชื่อว่า "แมวหรือหมา"
        cat_or_dog_poll = self.browser.find_element(By.LINK_TEXT, "แมวหรือหมา")
        # ปาร์คกดเข้าไปที่ลิงค์
        cat_or_dog_poll.click()
        # ปาร์คเห็นว่ามีปุ่มสองปุ่ม (แมว กับ หมา)
        catBtn = self.browser.find_element(By.ID, "แมว")
        dogBtn = self.browser.find_element(By.ID, "หมา")
        catBtn.is_displayed()
        dogBtn.is_displayed()
        time.sleep(1)
        # ปาร์คกด หมา และกด submit
        dogBtn.click()
        self.browser.find_element(By.ID, "Submit Vote").click()
        # ปาร์คเห็นว่า หน้าเว็บเปลี่ยนไปและมีขึ้นว่า แมว => 11 หมา => 8
        catScore = self.browser.find_element(By.ID, "แมว")
        dogScore = self.browser.find_element(By.ID, "หมา")
        self.assertEqual(catScore.text, "แมว (1)")
        self.assertEqual(dogScore.text, "หมา (3)")
        time.sleep(1)

class testHotAndWarm(StaticLiveServerTestCase):
    def setUp(self):    
        self.poll_hot = Poll.objects.create(name="Hot Poll")
        self.poll_warm = Poll.objects.create(name="Warm Poll")
        self.poll_normal = Poll.objects.create(name="Normal Poll")
        
        self.choice1 = Choice.objects.create(poll=self.poll_hot, name="Choice1", vote_count=50)
        self.choice2 = Choice.objects.create(poll=self.poll_warm, name="Choice2", vote_count=10)
        self.choice3 = Choice.objects.create(poll=self.poll_normal, name="Choice3", vote_count=0)

        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()
    
    def test_poll_vote_and_classification(self):
        self.browser.get(self.live_server_url)
        
        # Check Hot Poll
        self.assertIn("[🔥 HOT] Hot Poll", self.browser.page_source)
        self.assertIn("[🔼 WARM] Warm Poll", self.browser.page_source)
        self.assertIn("Normal Poll", self.browser.page_source)
        
        # Click and vote for each category
        time.sleep(1)
        for poll_name in ["[🔥 HOT] Hot Poll", "[🔼 WARM] Warm Poll", "Normal Poll"]:
            poll_link = self.browser.find_element(By.LINK_TEXT, poll_name)
            poll_link.click()
            
            time.sleep(1)
            match poll_name:
                case "[🔥 HOT] Hot Poll":choice = "Choice1"
                case "[🔼 WARM] Warm Poll":choice = "Choice2"
                case "Normal Poll":choice = "Choice3"
            choice_button = self.browser.find_element(By.ID, choice)
            choice_button.click()
            
            self.browser.find_element(By.ID, "Submit Vote").click()
            time.sleep(1)
            # Check if vote count is updated correctly
        
            choice_label = self.browser.find_element(By.ID, choice)
            vote_count = int(choice_label.text.split("(")[1].split(")")[0])
            
            if poll_name == "Hot Poll":
                self.assertTrue(vote_count > 50)
            elif poll_name == "Warm Poll":
                self.assertTrue(vote_count > 10)
            else:
                self.assertTrue(vote_count >= 1)
            
            # Navigate back to home page
            home_button = self.browser.find_element(By.TAG_NAME, "button")
            home_button.click()
