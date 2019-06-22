import pickle
from users.models import Country, Institute

country_count = 0
inst_count = 0
def run():
    global inst_count
    global country_count

    uni_dict = pickle.load(open("uni_dict.pkl","rb"))

    for country in uni_dict.keys():

        c,_ = Country.objects.get_or_create(country=country)
        institutes = []
        inst_count = 0
        for inst in set(uni_dict[country]):

            try:
                institutes.append(Institute(country = c, institute = inst))
            except:
                print(country, inst)
        try:
            Institute.objects.bulk_create(institutes)
        except:
            print(Country, country)

        country_count+=1

    for inst in uni_dict["Bangladesh"]:
        c,_  = Country.objects.get_or_create(country = "Bangladesh")
        try:
            Institute.objects.create(country= c, institute = inst)
        except:
            print(inst)



