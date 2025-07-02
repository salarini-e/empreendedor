import requests
from bs4 import BeautifulSoup
from desenvolve_nf.models import ClimaTempo


def ClimaTempoTemperaturas():
    page = requests.get("https://www.climatempo.com.br/previsao-do-tempo/cidade/314/novafriburgo-rj")
    soup = BeautifulSoup(page.content, "html.parser")
    print(page.status_code)
    minTemp = soup.find(id="min-temp-1")
    maxTemp = soup.find(id="max-temp-1")
    print(minTemp.text, maxTemp.text)
    results = soup.find_all("div", class_='_center')
    climaList = []

    for result in results:
        children = result.findChildren("img" , recursive=False)
        try:
            altText = children[0]["alt"]
        except:
            continue
        climaList.append(altText.lower())
        
        # if altText.lower() == "noite com muitas nuvens":
        #     climaURL = 'static/icons/noite_nuvem.png'
        # elif altText.lower() == "sol com muitas nuvens":
        #     climaURL = 'static/icons/sol_nuvem_vento.png'
        # elif altText.lower() == "sol, pancadas de chuva e trovoadas" or altText.lower() == "noite com pancadas de chuva e trovoadas":
        #     climaURL = 'static/icons/tempestade.png'

        # climaList.append({altText: climaURL})

    clima = ClimaTempo(
        maxTemp = maxTemp.text.replace('°', ''),
        minTemp = minTemp.text.replace('°', ''),
        madrugada = climaList[0],
        manha =     climaList[1],
        tarde =     climaList[2],
        noite =     climaList[3])
    clima.save()
    print(clima)