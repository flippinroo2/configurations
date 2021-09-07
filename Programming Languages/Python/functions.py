def setup_logs(log_filename="log", log_format='%(levelname)s:Line # %(lineno)d:%(asctime)s - %(message)s'):
	"""Utility function to set up logging.

	Parameters
	----------
	log_filename - The name of the log file to create a handler for : type String
	log_format - The format to use when logging items : type String

	Returns
	---------
	log - The main log object used throughout the application : type Object
	"""

	log_file_path = f'{CURRENT_DIRECTORY}/custom_logs/{log_filename}'
	log_formatter = logging.Formatter(fmt=log_format, datefmt='%B %d, %Y  %H:%M')
	log_handler = logging.FileHandler(filename=log_file_path, mode='a', encoding=None, delay=False)
	log_handler.setFormatter(log_formatter)
	log = logging.getLogger()
	log.setLevel(logging.INFO)
	log.addHandler(log_handler)
	return log


def validate_json(json_string):
	try:
		json.loads(json_string)
	except Exception as e:
		LOG.exception(f"ERROR - {e}", exc_info=True)
		if DEBUG:
			print(f"ERROR - {e}")
		return False
	return True


def validate_json(json_string, encoding="utf-8"):
	"""Function to check if a string is valid JSON or not

	Parameters
	----------
	json_string - The input text that should be parsed into JSON : type String

	Returns
	---------
	A boolean dictating if the JSON was indeed valid or not : type Boolean
	"""

	try:
		json.loads(json_string)
	except Exception as e:
		EXCEPTIONS.append(e)
		print("INVALID JSON")
		return False
	return True


def request(url, http_method="get", payload={}, parsed=False):
	http_method = http_method.lower()
	try:
		if http_method == 'get':
			response = requests.get(url)
		elif http_method == 'post':
			response = requests.post(url, json=payload)
		elif http_method == 'put':
			response = requests.put(url, json=payload)
		elif http_method == 'delete':
			response = requests.delete(url)
		status_code = response.status_code
		if status_code == 403:
			LOG.error('HTTP Response 403: Forbidden')
			if DEBUG:
				print(f"HTTP Response 403: {url}")
		if status_code == 404:
			LOG.error('HTTP Response 404: Page Not Found')
			if DEBUG:
				print(f"HTTP Response 404: {url}")
		if parsed and validate_json(response.text):
			return json.loads(response.text)
	except Exception as e:
		LOG.exception(f'Exception: {e}', exc_info=True)
	return response


# TODO: Do something about the "weighted" parameter lol
def test_assert():
	"""Example of assert
  """
	upper_range = 100
	lower_range = 1
	assert lower_range < upper_range  # TODO: Re-factor to using the test files created in the "tests" directory

	like = 40
	comment = 50
	follow = 60
	unfollow = 70
	total = 1000
	total = max([like, comment, follow, total])
	assert total == max([like, comment, follow, total])


def download_webdrivers(chrome=True, firefox=False):
	"""This function reaches out to a repository containing WebDrivers for all of the browsers compatible with Selenium. This ensures that each run of this script receives a brand new, updated, WebDriver.

	:param chrome: boolean
	:param firefox: boolean
	:return webdriver_path: String - Path to directory containing appropriate WebDrivers.
	"""

	# TODO: Determine the current Chrome version on the machine, then get a matching WebDriver for that. (Going to be hard to do on multi platform. Found PyWin32 for Windows - http://www.blog.pythonlibrary.org/2014/10/23/pywin32-how-to-get-an-applications-version-number/)

	chrome_version_test1 = os.system("/Applications/Google\ Chrome.app --version")  # NOTE: This is the syntax for getting the Google Chrome version for Linux (https://linuxconfig.org/how-check-version-of-chrome)
	chrome_version_test2 = subprocess.call(["/Applications/Google\ Chrome.app", "--version"], shell=True)  # NOTE: Try using shell=True and try without

	user_directory = os.path.expanduser('~')
	webdriver_path = f'{CURRENT_DIRECTORY}/workspace/InstaPy/assets'
	try:
		if os.path.exists(webdriver_path):
			rmtree(webdriver_path)
		if chrome:
			chrome_driver = ChromeDriverDownloader()
			chrome_driver.download_root = webdriver_path
			chrome_driver.link_path = webdriver_path
			chrome_driver.download_and_install()
		if firefox:
			gecko_driver = GeckoDriverDownloader()
			gecko_driver.download_root = webdriver_path
			gecko_driver.link_path = webdriver_path
			gecko_driver.download_and_install()
		if chrome or firefox:  # NOTE: This runs right after the download occurs
			os.rmdir(f'{user_directory}/webdriver')
			os.rmdir(f'{user_directory}/bin')
	except Exception as e:
		LOG.error(f'Exception: {e}', exc_info=True)
	finally:
		return webdriver_path


def clean_list(dirty_list):
	cleaned_list = []
	dirty_list = list(set(filter(None, dirty_list)))  # NOTE: Removes duplicate entries and invalid items from list
	for dirty_item in dirty_list:
		if type(dirty_item) == str:
			clean_item = sub(r'\s', '', dirty_item)  # NOTE: Removes white space characters from the list item.
		else:
			clean_item = dirty_item
		cleaned_list.append(clean_item)
	return cleaned_list


def get_list_from_file(list_filename="master_proxy_list.txt"):
	with open(f'{CURRENT_DIRECTORY}/proxy_lists/{list_filename}', 'r+', encoding="utf-8") as f:
		list_from_file = f.readlines()
	return clean_list(list_from_file)


def overwrite_list_file(master_list):
	"""This function overwrites a file with a new list.
	"""

	with open(f'{CURRENT_DIRECTORY}/proxy_lists/master_proxy_list.txt', 'r+', encoding="utf-8") as f:
		f.seek(0)
		f.write("\n".join(clean_list(master_list)))
		f.truncate()


def output_list_to_file(output_list, output_filename=f"MASTER_LIST_{randint(1, 1000000)}.txt", output_directory="/"):
	if output_directory and output_directory != '/':
		with open(f'{CURRENT_DIRECTORY}{output_directory}/{output_filename}', 'a', encoding="utf-8") as f:
			# for clean_output in clean_list(output_list):
			for clean_output in output_list:
				print(clean_output, file=f)
	else:
		with open(f'{CURRENT_DIRECTORY}/{output_filename}', 'a', encoding='utf-8') as f:
			# for clean_output in clean_list(output_list):
			for clean_output in output_list:
				print(clean_output, file=f)


def verify_proxy(proxy):
	ip_address_websites = [
		'https://whatsmyip.org',
		'https://www.whatismyip.com',
		'https://whatismyipaddress.com'
	]
	proxies = {
		"http": f'http://{proxy}',
		"https": f'https://{proxy}'
	}
	for website in ip_address_websites:
		try:
			# NOTE: Look at the response when getting a HTTP 403: Forbidden because the IP address is in the footer of those pages (View url directly from browser)
			proxy_verification = requests.get(website, proxies=proxies)
			if proxy_verification.status_code == 200:
				if DEBUG:
					print(f"Website: {website} - Proxy: {proxy} - Response: {proxy_verification}")
				return True
		except Exception as e:
			LOG.exception(f"ERROR: {e}", exc_info=True)
			if DEBUG:
				print(f"ERROR: {e}")
	else:
		# TODO: Remove proxy from verified list (If it was valid the function would have already returned)
		return False


def get_proxy_location(proxy_ip):
	geolocation_apis = {
		"ip-api": {
			"endpoint": f"http://ip-api.com/json/{proxy_ip}?fields=regionName,city,zip",
			"http_request_method": "get"
		},
		# "ipgeolocationapi": {
		# 	"endpoint": f"https://api.ipgeolocationapi.com/geolocate/{proxy_ip}", "http_request_method": "get"
		# },
		"extreme-ip-lookup": {
			"endpoint": f"https://extreme-ip-lookup.com/json/{proxy_ip}",
			"http_request_method": "post",
			"payload": {}
		},
		"ipligence": {
			"endpoint": f"https://www.ipligence.com/geolocation/",
			"http_request_method": "post",
			"payload": {"ip": proxy_ip}
		},
		"db-ip": {
			"endpoint": f"http://api.db-ip.com/v2/free/{proxy_ip}",
			"http_request_method": "get"
		},
		"ipapi": {
			"endpoint": f"https://ipapi.co/{proxy_ip}/json/",
			"http_request_method": "get"
		}
	}
	state_entries = []
	for name, api in geolocation_apis.items():
		api_endpoint = api.get('endpoint')
		http_request_method = api.get('http_request_method', 'get')
		payload = api.get('payload', {})
		api_request = request(api_endpoint, http_request_method, payload)
		if api_request:
			api_response = api_request.text
			if validate_json(api_response):
				api_response = json.loads(api_response)
				if name == 'extreme-ip-lookup':
					state = api_response.get('region', '')
					if DEBUG:
						print(f"extreme-ip-lookup - {state}")
					state_entries.append(state)
				if name == 'ipligence':
					print("PAUSE")  # TODO: Need to get the request working properly instead of returning HTML. (Might be working now, need to test)
				if name == 'db-ip':
					state = api_response.get('stateProv', '')
					if DEBUG:
						print(f"db-ip - {state}")
					state_entries.append(state)
				if name == 'ip-api':
					state = api_response.get('regionName', '')
					if DEBUG:
							print(f"ip-api - {state}")
					state_entries.append(state)
				if name == 'ipapi':
					print("PAUSE")  # TODO: Need to get the request working properly
	return {
		"state": state,
		"state_entries": state_entries
	}


def filter_proxy_list(proxy_list, filters={"state": "florida"}):
	filtered_list = []
	for proxy in clean_list(proxy_list):
		proxy_ip = proxy.split(":")[0]
		proxy_location = get_proxy_location(proxy_ip)
		proxy_state_entries = proxy_location.get("state_entries", [])
		for proxy_state_entry in proxy_state_entries:
			if proxy_state_entry.lower() == filters.get("state", "").lower():
				filtered_list.append(proxy)
	return clean_list(filtered_list)


def get_dynamic_proxies():
	proxy_apis = {
		"proxyscrape": "https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=US&anonymity=elite&ssl=yes",  # NOTE: There's a "timeout" parameter that may help speed things up. (Test later maybe?)
		# "webshare": "https://proxy.webshare.io/api/proxy/stats/",  # NOTE: API KEY = os.getenv("WEBSHARE_IO_API_KEY") & Documentation - https://proxy.webshare.io/docs/#proxy
		"gimmeproxy": "https://gimmeproxy.com/api/getProxy?anonymityLevel=1&country=US&port=80"  # NOTE: May not need to include the port=80 part
	}
	dynamic_proxy_list = []
	for name, api in proxy_apis.items():
		try:
			proxy_api_response = request(api)
			if proxy_api_response.status_code == 200:
				response_text = proxy_api_response.text
				if validate_json(response_text):
					formatted_response = json.loads(response_text)
					if name == 'gimmeproxy':
						proxy = formatted_response.get('ipPort')
					dynamic_proxy_list.append(proxy)
					continue
				if response_text.splitlines():
					dynamic_proxy_list.extend(response_text.splitlines())
			continue
		except Exception as e:
			LOG.exception(f"ERROR: {e}", exc_info=True)
			if DEBUG:
				print(f"ERROR: {e}")
	return dynamic_proxy_list


def setup_webdriver_proxy_object(proxy_address=os.getenv("PROXY"), proxy_port=int(os.getenv("PORT"))):
	"""This function calls an API that returns proxy information. This API endpoint contains many proxies that are always changing / rotating. A new Proxy object is built based on the results of the proxy API endpoint response.

	:param proxy_address: String
	:param proxy_port: int or String
	:return proxy: selenium Proxy - A Proxy object configured to be inserted into a selenium WebDriver.
	"""

	dynamic_proxies = get_dynamic_proxies()
	add_proxies_to_list(dynamic_proxies, "master_proxy_list.txt")
	master_proxy_list = get_list_from_file("master_proxy_list.txt")
	overwrite_master_list_file(master_proxy_list)
	florida_proxy_list = filter_proxy_list(master_proxy_list)
	for florida_proxy in florida_proxy_list:
		if verify_proxy(florida_proxy):
			active_proxy = florida_proxy
			break
	[proxy_address, proxy_port] = active_proxy.split(":")
	proxy_object = webdriver.common.proxy.Proxy({
		'autodetect': False,  # NOTE: Would like to learn What this does?
		'proxyType': webdriver.common.proxy.ProxyType.MANUAL,  # NOTE: MANUAL, PAC, or AUTODETECT
		'httpPort': proxy_port,
		'httpProxy': active_proxy,
		'ftpProxy': active_proxy,
		'sslProxy': active_proxy,
		'noProxy': ''
	})
	return proxy_object


def setup_custom_webdriver():
	"""This function handles the building of the new WebDriver that will be replacing the default one created from InstaPy.

	:param proxy_address: String
	:param proxy_port: int or String
	:return proxy: selenium Proxy - A Proxy object configured to be inserted into a selenium WebDriver.
	"""

	# NOTE: Remote sessions are when the WebDriver is ran as a service beforehand, and then the client connects to that service at a later time. Could using a remote session help my issue with the InstaPy constructor?
	proxy_object = setup_webdriver_proxy()
	chrome_options = webdriver.ChromeOptions()
	chrome_options.Proxy = proxy_object
	chrome_options.add_argument("--mute-audio")
	chrome_options.add_argument("--dns-prefetch-disable")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--lang=en-US")
	chrome_options.add_argument("--disable-setuid-sandbox")
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument(f'--proxy-server=http://{proxy_object.http_proxy}')
	chrome_options.add_argument(f'--ignore-certificate-errors')
	chrome_options.add_argument(f'--allow-insecure-localhost')
	chrome_options.add_argument(f'--ignore-urlfetcher-cert-requests')
	browser_capabilities = chrome_options.to_capabilities()
	browser_capabilities["acceptSslCerts"] = browser_capabilities["acceptInsecureCerts"] = browser_capabilities["browserConnectionEnabled"] = browser_capabilities["javascriptEnabled"] = browser_capabilities["networkConnectionEnabled"] = True
	proxy_object.add_to_capabilities(browser_capabilities)
	# chrome_webdriver = webdriver.Chrome(executable_path=f'{WEBDRIVER_DIRECTORY}/chromedriver', options=chrome_options)
	chrome_webdriver = webdriver.Chrome(executable_path=f'{WEBDRIVER_DIRECTORY}/chromedriver', options=chrome_options, desired_capabilities=browser_capabilities)
	return chrome_webdriver


def parse_beautiful_soup_page(page_source):
	"""Function to take the current page's source code and parse it into a "BeautifulSoup" Python Object that has a lot of utility functions for extracting and modifying data.

	:param page_source: String
	:return: BeautifulSoup Object
	"""

	return BeautifulSoup(sub(r'\n|\r|\t', '', page_source), 'html.parser')


def custom_random_number(base=10):
	return round((random() * base) * (random() * base))


def random_sleep(seconds=5):
	upper_range = round((random() * seconds) * 10)
	random_number = randint(1, int(upper_range))
	if DEBUG:
		print(f'Sleeping for {random_number} seconds')
	sleep(random_number)


def create_spreadsheet(filename=f'instagram_data_{datetime.now().strftime("%m_%d_%Y")}.xlsx', sheets=[]):
	spreadsheet = Workbook(write_only=True, iso_dates=False)
	for sheet in sheets:
		add_sheet(spreadsheet, sheet)
	spreadsheet.filename = f"{CURRENT_DIRECTORY}/scraped_data/{filename}"
	return spreadsheet


def add_sheet(spreadsheet, sheet_name='MASTER'):
	default_font = Font(name="Calibri", size=12, bold=False, italic=False, vertAlign=None, underline="none", strike=False, color="FF000000")
	# default_border = Border()
	default_alignment = Alignment(horizontal="general", vertical="center", text_rotation=0, wrap_text=False, shrink_to_fit=False, indent=0)
	if sheet_name in spreadsheet.sheetnames:
		sheet = spreadsheet.active(sheet_name)
	else:
		sheet = spreadsheet.create_sheet(sheet_name)
	sheet.font = default_font
	sheet.alignment = default_alignment
	sheet_properties = sheet.sheet_properties
	sheet_properties.filterMode = True
	sheet_properties.pageSetUpPr = PageSetupProperties(autoPageBreaks=False, fitToPage=True)
	sheet_properties.pageSetUpPr.autoPageBreaks = True  # NOTE: Wonder why we set "False" in constructor then change it here? (This is how it was done in the example)
	return sheet


def write_data_to_sheet(sheet, data_list, headers=False):
	new_data = []
	data_list_count = len(data_list)
	if headers:
		sheet.append(headers)
	else:
		sheet.append([f'column_{x + 1}' for x in range(data_list_count)])
	for i, value in enumerate(data_list):  # NOTE: Might need to use the "any()" function here.
		if DEBUG:
			print(f'Index = {i}\n Value = {value}')
		if isinstance(value, str):
			print("PAUSE")
		elif isinstance(value, list):
			if isinstance(data_list[i + 1], list):
				new_data = (itertools.zip_longest(*data_list, fillvalue=""))
				break
			new_data = [new_data, *data_list]
		elif isinstance(value, dict):
			new_data.append([value.get("post_id", "N/A")])
			for key, val in value.items():
				if isinstance(val, str):
					print("PAUSE")
				if isinstance(val, list):
					new_data.append([key, *[x for x in val]])
		else:
			continue
	for data in new_data:
		sheet.append(data)


def remove_duplicate_tuple(data):
	"""Function that ensures no 2 tuples have the same second element.

	Parameters
	----------
	data - The list of tuples to analyze for duplicates : type list

	Returns
	---------
	new list of tuples without any duplicate second entries : type list
	"""

	# Creating an empty set
	temp_set = set()

	# Output list initialization
	output_list = []

	# Iteration
	for a, b in data:
		if b not in temp_set:
			temp_set.add(b)
			output_list.append((a, b))
	return output_list


def format_time(time):
	"""Function to format dates in ISO format with 3 digits for microseconds (required by ARC).

	Parameters
	----------
	time - The time to be formatted : type String, Date, Datetime

	Returns
	---------
	Formatted time : type String
	"""

	if isinstance(time, str):
		time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%fZ')
	return f'{time.isoformat(timespec="milliseconds")}Z'


# NOTE: Process escape sequences inside of a raw string - https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python#answer-24519338
ESCAPE_SEQUENCE_RE = re.compile(r'''
		( \\U........      # 8-digit hex escapes
		| \\u....          # 4-digit hex escapes
		| \\x..            # 2-digit hex escapes
		| \\[0-7]{1,3}     # Octal escapes
		| \\N\{[^}]+\}     # Unicode characters by name
		| \\[\\'"abfnrtv]  # Single-character escapes
		)''', re.UNICODE | re.VERBOSE)


def decode_control_characters(s):
	def decode_match(match):
		return codecs.decode(match.group(0), 'unicode-escape')
	return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


def check_for_404_response():
	print("PAUSE")


@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
def throttled_request(url, request_method='get', payload={}, parsed=True):
	"""Function to throttle requests to ARC sandbox.

	Decorators
	----------
	sleep_and_retry - Instructions on what to do if the maximum number of requests is reached.
	limits(calls, period) - Setting the limit on how many times this function can run per specified amount of time.
		calls: The maximum number of requests to make
		period: The time period allocated for the number of calls

	Parameters
	----------
	url - The URL to send a HTTP request to : type String
	request_method - The HTTP request method to use on the provided URL : type String
	payload (optional) - The data to be send with an HTTP request : type Dictionary

	Returns
	---------
	HTTP response : type Object
	"""

	request_method = request_method.lower()  # NOTE: Making this lowercase to avoid syntax errors.
	try:
		if request_method == 'get':
			response = requests.get(url)
		elif request_method == 'post':
			response = requests.post(url, json=payload)
		elif request_method == 'put':
			response = requests.put(url, json=payload)
		elif request_method == 'delete':
			response = requests.delete(url)
		status_code = response.status_code
		if status_code == 201:
			if DEBUG:
				LOG.info('HTTP Response 201: Created')
				LOG.info(f'HTTP Response Text: {response.text}')
		if status_code == 204:
			with open(f'{CURRENT_DIRECTORY}/url_lists/204_RESPONSE_URL_LIST.txt', 'a', encoding='utf-8') as f:
				print(url, file=f)
			LOG.warning('HTTP Response 204: No Content')
			if DEBUG:
				LOG.info(f'HTTP Response Text: {response.text}')
			return response
		if status_code == 400:
			LOG.error('HTTP Response 400: Invalid ANS Story')
			LOG.info(f'ARTICLE DATA - articleId: {payload.get("articleId", payload.get("publishDate", "NO articleId or publishDate"))}')
			if DEBUG:
				LOG.info(f'HTTP Response Text: {response.text}')
			# raise Exception("TEST")
		if status_code == 404:
			with open(f'{CURRENT_DIRECTORY}/url_lists/404_RESPONSE_URL_LIST.txt', 'a', encoding='utf-8') as f:
				print(url, file=f)
			if DEBUG:
				LOG.error('HTTP Response 404: Page Not Found')
				LOG.info(f'ARTICLE DATA - articleId: {payload.get("articleId", payload.get("publishDate", "NO articleId or publishDate"))}')
			# LOG.info(f'HTTP Response Text: {response.text}')
			return response
		if status_code == 429:
			LOG.error(f"HTTP Response 429: {ENVIRONMENT.title()} has exceeded it's rate limit. Currently running {CALLS} articles per {PERIOD} seconds")
			LOG.info(f'HTTP Response Text: {response.text}')
			return response
		if parsed:
			if validate_json(response.text):
				return response.json()
	except Exception as e:
		with open(f'{CURRENT_DIRECTORY}/url_lists/EXCEPTION_RESPONSE_URL_LIST.txt', 'a', encoding='utf-8') as f:
				print(url, file=f)
		EXCEPTIONS.append(e)
		LOG.exception(f'Exception: {e}')
		return response
	return response


def url_filter(filter_item):
	"""Function to filter out invalid url items from a list. This function is mainly used as a parameter for the built-in "filter()" function in Python.

	Parameters
	----------
	filter_item - A list item to be checked for validity. This is passed in automatically from the "filter()" function in Python : type String

	Returns
	---------
	If the list item is valid or not : type Boolean
	"""

	if filter_item:
		if filter_item == "\n" or filter_item.find("<!--") != -1:  # TODO: Maybe expand on these invalid character checks
			return False
	return True


def clean_url_list(url_list):
	"""Cleans a list of urls to ensure they don't have spaces, don't have duplicates, and semi-checks for invalid entries. (See "url_filter()" function above)

	Parameters
	----------
	url_list - A list of URLs in String format : type List

	Returns
	---------
	cleaned_url_list - A cleaned list of urls : type List
	"""

	cleaned_url_list = []
	url_list = list(set(filter(url_filter, url_list)))  # NOTE: Removes duplicate entries and invalid items from list
	for url in url_list:
		cleaned_url = re.sub(r'\s', '', url)  # NOTE: Removes white space characters from the url (Space, Tab, New Line)
		cleaned_url_list.append(cleaned_url)
	return cleaned_url_list


def get_list_from_text_file(filename='DEFAULT_FILE_NAME.txt', directory_name='', cleaned=False):
	"""Generates a Python list from a text file that contains article URLs. (One URL per line)

	Parameters
	----------
	filename - The name of the text file that contains the URL list : type String
	directory_name - An optional parameter to tell the script to look into a different directory : type String

	Returns
	---------
	A Python list of URLs : type List
	"""

	if directory_name and directory_name != '/':
		with open(f'{CURRENT_DIRECTORY}/{directory_name}/{filename}', 'r', encoding='utf-8') as f:
			if cleaned:
				return clean_url_list(f.readlines())
			return f.readlines()
	with open(f'{CURRENT_DIRECTORY}/{filename}', 'r', encoding='utf-8') as f:
		if cleaned:
			return clean_url_list(f.readlines())
		return f.readlines()


def output_list_to_text_file(output_list, filename=f'DEFAULT_FILE_NAME_{format_time(datetime.now()).split("T")[0]}.txt', directory_name=''):
	"""Builds the content elements in the ANS (ARC native spec) format.

	Parameters
	----------
	output_list - The list of items to be output to a text file  : type List
	filename - The name of the output file : type String
	directory_name - An optional parameter to determine which directory a file should be written to : type String

	Returns
	---------
	N/A : type Void
	"""

	if directory_name and directory_name != '/':
		with open(f'{CURRENT_DIRECTORY}{directory_name}/{filename}', 'a', encoding='utf-8') as f:
			f.write("\n".join(output_list))  # Alternative method of outputting a list into a file in 1 line.
	else:
		with open(f'{CURRENT_DIRECTORY}/{filename}', 'a', encoding='utf-8') as f:
			for clean_output in clean_url_list(output_list):
				print(clean_output, file=f)


def prepend_url_with_slash(path):
	"""Ensure that a url begins with a slash

	Parameters
	----------
	path - A news article's url path : type String

	Returns
	---------
	A formatted string of the sectionPath : type String
	"""

	return f'/{path.strip("/")}'


def wrap_url_with_slashes(path):
	"""Adds a trailing slash to the section path and used to output url in the put_payload

	Parameters
	----------
	path - A news article's url path : type String

	Returns
	---------
	A formatted string of the sectionPath : type String
	"""

	if path:
		return f'/{path.strip("/")}/'


def create_scc_url(text, publish_date):
	"""Builds URL for SCC stories based on publish date.

	Parameters
	----------
	text - The : type String
	publish_date - The date an article was first published : type String

	Returns
	---------
	The formatted URL for articles within SCC : type String
	"""

	date = datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%SZ")
	day = f'{date.day:02d}'
	month = f'{date.month:02d}'
	url = f'/archive/{str(date.year)}/{month}/{day}/{slugify(text)}/'
	return url


def upload_json_to_s3(article_data, source):
	"""Utility function to upload a JSON object to the ARC ("sandbox" or "production") S3 bucket.

	Parameters
	----------
	article_data - A news article's data : type Dictionary
	source - The source of the news article's data (either "NEWSCYCLE" or "SCC") : type String

	Returns
	---------
	A UUID for the newly created image : type String
	"""

	global ENVIRONMENT, IMAGES_ADDED
	s3 = boto3.resource('s3')
	if DEBUG and (ENVIRONMENT == 'sandbox'):
		bucket_name = 'tpc-shared'
		folder_name = 'ARC Image Test/'
	else:
		bucket_name = f'arc-anglerfish-arc2-{ENVIRONMENT}-bulk-import-tbt'
		folder_name = ''
	domain = 'https://ttt-hiweb.newscyclecloud.com'
	output = []
	images = []
	if SOLR:
		for index, value in enumerate(article_data.get('imagePhoto', [])):
			new_image_path = f'{domain}{urlparse(value).path}'  # TODO: Verify that single images that don't come in lists are handled.
			images.append({
				'photo': new_image_path,
				'caption': fix_text(article_data.get('imageCaption', [])[index]),
				'credits': fix_text(article_data.get('imageCredit', [])[index])
			})
	else:
		new_image_path = f'{domain}{urlparse(article_data.get("imagePhoto", "")).path}'  # TODO: Verify that single images that don't come in lists are handled.
		images.append({
			'photo': new_image_path,
			'caption': fix_text(article_data.get('imageCaption')),
			'credits': fix_text(article_data.get('imageCredit'))
		})
	for value in images:
		# Change the image path to use tampabay.com directly instead of using the "TTT-HIDEV" URL.
		image_url = value.get('photo', '')
		image_id = image_url[image_url.rfind("/") + 1: image_url.rfind(".")]
		image_uuid = six.text_type(base64.b32encode(uuid.uuid1().bytes), encoding='utf-8').replace('=', '')
		image_extension = image_url[image_url.rfind('.'):] or ".jpg"  # Check if removing the "." in .jpg here
		# image_extension = image_url[image_url.rfind('.'):image_url.find('&')] or ".jpg"  # Check if removing the "." in .jpg here
		image_caption = fix_text(value.get('caption', ''))
		image_credits = fix_text(value.get('credits', ''))
		filename = folder_name + image_url[image_url.rfind("/") + 1: image_url.rfind(".")] + ".json"
		s3.Object(bucket_name, filename).put(ACL='public-read', Body=json.dumps({
			"_id": image_uuid,
			"type": "image",
			"additional_properties": {
				"ingestionMethod": "Ingestor",
				"originalName": f'{image_id}{image_extension}',
				"originalUrl": image_url,
				"published": True,
				"version": 1
			},
			"caption": image_caption,
			"credits": {
				"by": [
					{
						"additional_properties": {},
						"name": image_credits,
						"type": "author"
					}
				]
			},
			"distributor": {
				"category": "other",
				"subcategory": "Ingestor",
				"mode": "custom",
				"name": "Archive"
			},
			"source": {
				"name": source,
				"source_id": article_data.get('articleId', ''),
				"source_type": "Ingestor"
			},
			"owner": {
				"id": "sandbox.tbt" if ENVIRONMENT == 'sandbox' else "tbt"
			},
		}))
		IMAGES_ADDED += 1
		output.append(image_uuid)
	return output


def prepend_text_to_list_file(list_filename, text_to_prepend):
	"""Prepends the passed in text to each item in the list. This list happens to come from a file....for now.

	Parameters
	----------
	list_filename - The name of the text file with a list of items in it : type String
	text_to_prepend - The text to prepend to each item in the list : type String

	Returns
	---------
	N/A : type Void
	"""

	list_from_file = get_list_from_text_file(list_filename)
	cleaned_list_from_file = clean_url_list(list_from_file)
	prepended_list = []
	error_list = []
	for item in cleaned_list_from_file:
		first_character = item[0]
		if first_character == "/":
			prepended_list.append(f'{text_to_prepend}{item}')
			continue
		if first_character == "b":
			error_list.append(f'{item}')  # TODO: Do something to handle the errors in this list.
			continue
		prepended_list.append(f'{text_to_prepend}/{item}')
	output_list_to_text_file(prepended_list, f'PREPENDED_{list_filename}')
	# return prepended_list
