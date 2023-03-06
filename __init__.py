import json
import os
import requests

api_key = os.environ["FLOWALTO_NUBELA_APIKEY"]

# Returns a LinkedIn URL based on a company name, web domain.
def search_company_linkedin_url(company_name, company_domain):
    result = requests.get("https://nubela.co/proxycurl/api/linkedin/company/resolve",
                      headers={"Authorization": "Bearer " + api_key},
                      params={
                          "company_name": company_name,
                          "company_domain": company_domain
                      })

    return(json.loads(result.text)["url"])

# Returns a JSON object with LinkedIn company information
def company_details_from_linkedin_url(company_linkedin_url):
    results = requests.get("https://nubela.co/proxycurl/api/linkedin/company",
                      headers={"Authorization": "Bearer " + api_key},
                     params={
                         "resolve_numeric_id": "true",
                         "categories": "exclude",
                         "funding_data": "exclude",
                         "extra": "exclude",
                         "exit_data": "exclude",
                         "acquisitions": "exclude",
                         "url": company_linkedin_url,
                         "use_cache": "if-present",
                     })
    return(json.loads(results.text))

# Looks up email given a LinkedIn profile URL.
# to-do: Using the Nubela interface for now, but could use queuing.
def email_lookup_by_linkedin_profile_url(linkedin_profile_url):
    result = requests.get("https://nubela.co/proxycurl/api/linkedin/profile/email",
                      headers={"Authorization": "Bearer " + api_key},
                      params={
                          "linkedin_profile_url": linkedin_profile_url
                      })

    return(result.text)

class Company:
    def __init__(self, company_name, company_domain):
        self.company_name = company_name
        self.company_domain = company_domain

    def company_details(self):
        company_linkedin_url = search_company_linkedin_url(company_name=self.company_name, company_domain=self.company_domain)
        if company_linkedin_url is not None:
            self.company_details = company_details_from_linkedin_url(company_linkedin_url=company_linkedin_url)
            return(self.company_details)
        else:
            return({""})

