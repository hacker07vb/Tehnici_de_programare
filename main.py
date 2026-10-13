from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

print("Partea 1, build_url simplu:", build_url("example.com", "login"))
print("Partea 1, build_url cu slash:", build_url("example.com", "/login"))
print("Partea 1, is_https cu https:", is_https("https://example.com"))
print("Partea 1, is_https cu http:", is_https("http://example.com"))

print("\nPartea 2, show_response functional:")
show_response("https://example.com")
print("Partea 2, show_response 404:")
show_response("https://httpbin.org/status/404")

print("\nPartea 3, check_site ok:", check_site("https://example.com"))
print("Partea 3, check_site picat:", check_site("http://this-site-does-not-exist.invalid"))

print("\nPartea 4, scan_sites:")
scan_sites()

print("\nPartea 5, check_headers cu securitate:", check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("Partea 5, check_headers fara securitate:", check_headers("https://example.com"))
print("Partea 5, check_headers picat:", check_headers("http://this-site-does-not-exist.invalid"))

print("\nPartea 6, retry_check status 200:", retry_check("https://httpbin.org/status/200"))
print("Partea 6, retry_check status 404:", retry_check("https://httpbin.org/status/404"))
print("Partea 6, retry_check status 500:", retry_check("https://httpbin.org/status/500"))
print("Partea 6, retry_check conexiune picata:", retry_check("http://this-site-does-not-exist.invalid"))