SEARCH_CONFIG = {

    "locations": ["Mumbai"],

    "required_keywords": [
        "customer care",
        "customer service",
        "customer support"
    ],

    "excluded_keywords": [
        "field sales",
        "delivery"
    ]

}

SOURCE_URLS = {
    "Apna": "https://apna.co/jobs?search=true&text=Customer+Care+Executive",
    "Job Hai": "https://www.jobhai.com/customer-care-representative-jobs-in-mumbai-cjrl"
}

SOURCE_CONFIG = {
    "Apna": {
        "url": SOURCE_URLS["Apna"]
    },

    "Job Hai": {
        "url": SOURCE_URLS["Job Hai"]
    }
}
