import requests
import json
from django_cron import CronJobBase, Schedule
from myfoodapp.models import Food

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'foodbapp.my_cron_job'    # a unique code

    def charposition(string, char):
        pos = [] #list to store positions for each 'char' in 'string'
        for n in range(len(string)):
            if string[n] == char:
                pos.append(n)
        return pos

    
    def changeurl(url):
        lespos = MyCronJob.charposition(url, '/')
        old_link = url
        old_link = old_link[0:lespos[-1]]
        new_link = old_link[:lespos[2]]+"/api/v0"+old_link[lespos[2]:]
        new_link = new_link+".json"
        return new_link

    def do(self):
        link = Food.objects.values_list('link_food', flat=True)
        total = len(link)
        i = 0
        for pos in link:
            i = i + 1
            # print(pos)
            url = MyCronJob.changeurl(pos)

            temp = Food.objects.filter(link_food=pos).values(
                'dangers_food', 'nutri_score_food', 'quantity_food','img_food',
                'store_food')
            
            dangers_food = temp[0]['dangers_food']
            nutri_score_food = temp[0]['nutri_score_food']
            store_food = temp[0]['store_food']
            quantity_food = temp[0]['quantity_food']
            img_food = temp[0]['img_food']

            response = requests.get(url)
            update = False
            if(response.ok):    # if answer is ok we take info
                jData = json.loads(response.content)
                quantity = str(jData.get('product').get('quantity'))
                quantity = quantity.replace('\\', '')
                if quantity != quantity_food:
                    Food.objects.filter(link_food=pos).update(quantity_food=quantity)
                    update = True

                dangers = str(jData.get('product').get('traces'))
                dangers = dangers.replace('\\', '')
                if dangers != dangers_food:
                    Food.objects.filter(link_food=pos).update(dangers_food=dangers)
                    update = True

                stores = str(jData.get('product').get('stores'))
                stores = stores.replace('\\', '')
                if stores != store_food:
                    Food.objects.filter(link_food=pos).update(store_food=stores)
                    update = True

                nutri_score = str(jData.get('product').get('nutrition_grades_tags')[0])
                nutri_score = nutri_score.replace('\\', '')
                if nutri_score != nutri_score_food:
                    Food.objects.filter(link_food=pos).update(nutri_score_food=nutri_score)
                    update = True

                img = str(jData.get('product').get('image_url'))
                if img != img_food:
                    Food.objects.filter(link_food=pos).update(img_food=img)
                    update = True

                if update:
                    print(pos+"  has been updated")

            progression = i*100/total
            print("prog is : "+str(progression)+"%")