Capturing the evolution of public sector Covid19 response sites from around
the world. Lots of governments have responded quickly and used the web to
provide essential information, and analysing how they have done will be a
useful indicator of how well they're set up for internet-era ways of working.

This was started with a list from [the Public Digital blog](https://public.digital/2020/03/18/making-things-open-is-making-things-better/)

For each site I'm capturing:

* A screenshot
* A report from [lighthouse](https://developers.google.com/web/tools/lighthouse) in both HTML and JSON

The former will show how the sites evolve in terms of the content they prioritise and
the visual design to support it. The latter will show how accessible those sites are.

They're stored in a way that was convenient to me when capturing them, which
may not be the easiest structure for analysis. If you want to use this data and there's
another structure that would make it easier for you, let me know.

## Analysis

(April 23rd 2020) To start looking at what the data shows us, I've done some very
rough rankings based on the lighthouse scores for accessibility and performance.

Please take them as an experiment. There are many factors to look at more closely.
For example: I've not yet looked at the variance between the highest reported
scores and the averages to see what's going on, or done anything to control for
the fact that all requests originate in the UK.


### Test rankings for accessibility

| URL | Highest score | Average score |
| --- | --- | --- |
|  https://covid19.govt.nz/  |  1  |  0.835333333333  |
|  https://www.gov.uk/coronavirus  |  1  |  1.0  |
|  https://www.gov.scot/coronavirus-covid-19/  |  0.96  |  0.96  |
|  https://www.nhs.uk/conditions/coronavirus-covid-19/  |  0.95  |  0.922  |
|  https://coronavirus.idaho.gov/  |  0.94  |  0.927142857143  |
|  https://dhss.delaware.gov/dhss/dph/index.html  |  0.94  |  0.93  |
|  https://www2.gnb.ca/content/gnb/en/departments/ocmoh/cdc/content/respiratory_diseases/coronavirus.html  |  0.94  |  0.94  |
|  https://www.london.gov.uk/about-us/organisations-we-work/london-prepared  |  0.94  |  0.94  |
|  https://www.coronavirus.in.gov/  |  0.92  |  0.92  |
|  https://www2.hse.ie/coronavirus/  |  0.92  |  0.92  |
|  https://coronavirus.in.gov/  |  0.92  |  0.92  |
|  https://www.folkhalsomyndigheten.se/the-public-health-agency-of-sweden/communicable-disease-control/covid-19/  |  0.91  |  0.91  |
|  https://www.fhi.no/en/op/novel-coronavirus-facts-advice/  |  0.9  |  0.830666666667  |
|  https://www.government.nl/topics/coronavirus-covid-19  |  0.9  |  0.822  |
|  https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html  |  0.9  |  0.9  |
|  https://phpa.health.maryland.gov/Pages/Novel-coronavirus.aspx  |  0.9  |  0.895333333333  |
|  https://manitoba.ca/covid19/  |  0.9  |  0.9  |
|  https://www.ontario.ca/page/2019-novel-coronavirus  |  0.9  |  0.9  |
|  https://llyw.cymru/coronafeirws  |  0.89  |  0.888666666667  |
|  https://www.doh.wa.gov/Coronavirus/Workplace  |  0.89  |  0.89  |
|  https://www.mscbs.gob.es/en/profesionales/saludPublica/ccayes/alertasActual/nCov-China/home.htm  |  0.88  |  0.88  |
|  https://www.healthvermont.gov/response/infectious-disease/2019-novel-coronavirus  |  0.88  |  0.88  |
|  https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19  |  0.88  |  0.88  |
|  https://www.gov.nl.ca/covid-19/  |  0.87  |  0.846  |
|  https://health.ri.gov/covid/  |  0.86  |  0.8  |
|  https://www.london.gov.uk/what-we-do/fire-and-resilience/london-resilience-partnership  |  0.86  |  0.86  |
|  https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/  |  0.85  |  0.85  |
|  https://portal.ct.gov/coronavirus  |  0.85  |  0.85  |
|  https://health.mo.gov/living/healthcondiseases/communicable/novel-coronavirus/  |  0.84  |  0.821333333333  |
|  https://www.alberta.ca/coronavirus-info-for-albertans.aspx  |  0.84  |  0.84  |
|  https://www.doh.wa.gov/emergencies/coronavirus  |  0.83  |  0.782  |
|  https://www.nhsinform.scot/coronavirus  |  0.83  |  0.83  |
|  http://www.mohw.go.kr/react/index.jsp  |  0.83  |  0.755714285714  |
|  https://en.ssi.dk/  |  0.81  |  0.81  |
|  https://www.bag.admin.ch/bag/en/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov.html#903671355  |  0.81  |  0.81  |
|  https://sf.gov/topics/coronavirus-covid-19  |  0.81  |  0.77  |
|  https://www.michigan.gov/coronavirus  |  0.81  |  0.802666666667  |
|  https://www.healthvermont.gov/response/coronavirus-covid-19  |  0.81  |  0.81  |
|  https://coronavirus.health.ny.gov/home  |  0.81  |  0.81  |
|  https://coronavirus.utah.gov/  |  0.8  |  0.798  |
|  https://www.oesterreich.gv.at/public.html  |  0.8  |  0.8  |
|  https://www.argentina.gob.ar/salud/coronavirus-COVID-19  |  0.8  |  0.728  |
|  https://www.gob.pe/coronavirus  |  0.76  |  0.76  |
|  http://www.bccdc.ca/health-info/diseases-conditions/covid-19  |  0.75  |  0.592  |
|  https://www.gouvernement.fr/en/coronavirus-covid-19  |  0.74  |  0.74  |
|  http://www.health.go.ke/covid-19/  |  0.74  |  0.710909090909  |
|  https://novascotia.ca/coronavirus/  |  0.72  |  0.72  |
|  http://www.health.go.ke/  |  0.7  |  0.7  |
|  https://www.gov.sg/features/covid-19  |  0.69  |  0.654  |
|  https://covid19.ncdc.gov.ng/  |  0.67  |  0.67  |
|  https://arkartassituacija.gov.lv/  |  0.67  |  0.67  |
|  https://www.health.go.ug/covid/  |  0.64  |  0.64  |
|  https://coronavirus.ohio.gov/wps/portal/gov/covid-19/home  |  0.63  |  0.63  |
|  https://www.bundesgesundheitsministerium.de/coronavirus.html  |  0.62  |  0.601333333333  |
|  https://www.covid.is/english  |  0.61  |  0.6  |
|  https://www.info-coronavirus.be/fr/  |  0.51  |  0.484  |
|  https://www.gouv.bj/coronavirus/  |  0.38  |  0.38  |

### Test rankings for performance

| URL | Highest score | Average score |
| --- | --- | --- |
|  https://www.folkhalsomyndigheten.se/the-public-health-agency-of-sweden/communicable-disease-control/covid-19/  |  1  |  0.994666666667  |
|  https://www.info-coronavirus.be/fr/  |  0.99  |  0.742666666667  |
|  https://www.nhs.uk/conditions/coronavirus-covid-19/  |  0.97  |  0.962666666667  |
|  https://www.gov.uk/coronavirus  |  0.94  |  0.936666666667  |
|  https://en.ssi.dk/  |  0.92  |  0.857333333333  |
|  https://llyw.cymru/coronafeirws  |  0.92  |  0.858  |
|  https://www.government.nl/topics/coronavirus-covid-19  |  0.91  |  0.894  |
|  https://www.covid.is/english  |  0.91  |  0.871333333333  |
|  https://www.oesterreich.gv.at/public.html  |  0.91  |  0.838  |
|  https://www.gov.scot/coronavirus-covid-19/  |  0.87  |  0.851333333333  |
|  https://www.gouv.bj/coronavirus/  |  0.85  |  0.792666666667  |
|  https://www.bundesgesundheitsministerium.de/coronavirus.html  |  0.76  |  0.585333333333  |
|  https://www.london.gov.uk/about-us/organisations-we-work/london-prepared  |  0.75  |  0.75  |
|  https://www.fhi.no/en/op/novel-coronavirus-facts-advice/  |  0.74  |  0.691333333333  |
|  https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/  |  0.74  |  0.694666666667  |
|  https://www.healthvermont.gov/response/coronavirus-covid-19  |  0.74  |  0.71  |
|  https://www.london.gov.uk/what-we-do/fire-and-resilience/london-resilience-partnership  |  0.73  |  0.659230769231  |
|  https://sf.gov/topics/coronavirus-covid-19  |  0.72  |  0.663333333333  |
|  https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html  |  0.72  |  0.656  |
|  https://arkartassituacija.gov.lv/  |  0.72  |  0.692  |
|  https://health.mo.gov/living/healthcondiseases/communicable/novel-coronavirus/  |  0.65  |  0.596666666667  |
|  https://novascotia.ca/coronavirus/  |  0.64  |  0.635  |
|  https://www.bag.admin.ch/bag/en/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov.html#903671355  |  0.61  |  0.511333333333  |
|  https://www.nhsinform.scot/coronavirus  |  0.6  |  0.543333333333  |
|  https://www.ontario.ca/page/2019-novel-coronavirus  |  0.57  |  0.48  |
|  https://www2.hse.ie/coronavirus/  |  0.53  |  0.487333333333  |
|  https://www.alberta.ca/coronavirus-info-for-albertans.aspx  |  0.5  |  0.434666666667  |
|  https://www2.gnb.ca/content/gnb/en/departments/ocmoh/cdc/content/respiratory_diseases/coronavirus.html  |  0.49  |  0.457333333333  |
|  https://www.mscbs.gob.es/en/profesionales/saludPublica/ccayes/alertasActual/nCov-China/home.htm  |  0.47  |  0.322  |
|  https://www.gouvernement.fr/en/coronavirus-covid-19  |  0.47  |  0.346666666667  |
|  https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19  |  0.47  |  0.324666666667  |
|  https://covid19.govt.nz/  |  0.44  |  0.290666666667  |
|  https://www.gob.pe/coronavirus  |  0.44  |  0.365333333333  |
|  https://www.argentina.gob.ar/salud/coronavirus-COVID-19  |  0.42  |  0.365333333333  |
|  https://coronavirus.health.ny.gov/home  |  0.42  |  0.202666666667  |
|  https://covid19.ncdc.gov.ng/  |  0.41  |  0.334  |
|  https://coronavirus.utah.gov/  |  0.4  |  0.334  |
|  https://portal.ct.gov/coronavirus  |  0.39  |  0.160666666667  |
|  https://www.gov.sg/features/covid-19  |  0.36  |  0.276666666667  |
|  http://www.bccdc.ca/health-info/diseases-conditions/covid-19  |  0.36  |  0.248  |
|  https://manitoba.ca/covid19/  |  0.35  |  0.307333333333  |
|  https://www.health.go.ug/covid/  |  0.32  |  0.282666666667  |
|  http://www.health.go.ke/covid-19/  |  0.28  |  0.233636363636  |
|  https://www.gov.nl.ca/covid-19/  |  0.27  |  0.167333333333  |
|  https://www.healthvermont.gov/response/infectious-disease/2019-novel-coronavirus  |  0.24  |  0.235  |
|  http://www.mohw.go.kr/react/index.jsp  |  0.24  |  0.21  |
|  https://coronavirus.in.gov/  |  0.18  |  0.166666666667  |
|  https://www.michigan.gov/coronavirus  |  0.17  |  0.137333333333  |
|  https://dhss.delaware.gov/dhss/dph/index.html  |  0.17  |  0.098  |
|  https://health.ri.gov/covid/  |  0.13  |  0.119285714286  |
|  https://www.doh.wa.gov/Coronavirus/Workplace  |  0.13  |  0.121333333333  |
|  https://www.coronavirus.in.gov/  |  0.12  |  0.0975  |
|  https://coronavirus.ohio.gov/wps/portal/gov/covid-19/home  |  0.07  |  0.0533333333333  |
|  https://phpa.health.maryland.gov/Pages/Novel-coronavirus.aspx  |  0.07  |  0.054  |
|  https://coronavirus.idaho.gov/  |  0.06  |  0.0571428571429  |
|  https://www.doh.wa.gov/emergencies/coronavirus  |  0.04  |  0.0313333333333  |
|  http://www.health.go.ke/  |  0.01  |  0.01  |
