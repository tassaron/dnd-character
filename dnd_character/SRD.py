"""
A cached function that gets SRD data from a DND 5e REST API
"""
import json
from os import environ, walk, path, remove, mkdir
import logging


LOG = logging.getLogger(__package__)
LOG.setLevel(logging.DEBUG)


try:
    JSON_CACHE = f"{path.dirname(path.abspath(__file__))}/json_cache"
    if not path.exists(JSON_CACHE):
        mkdir(JSON_CACHE)

except Exception as e:
    LOG.error(f"Entire JSON cache failed to load: {str(e)}")


def cached_json(func):
    """
    Decorator which caches REST get requests into a dict
    and saves them to JSON files so the cache can be reloaded
    """
    func.cache = {}
    for dirname, __, files in walk(JSON_CACHE):
        for fp in files:
            if path.splitext(fp)[1] != ".json":
                continue
            try:
                with open(f"{dirname}/{fp}", "r") as f:
                    data = json.load(f)
                func.cache[f"/{fp.replace('_', '/')[:-5]}"] = data
            except json.decoder.JSONDecodeError as e:
                LOG.error(f"{fp} failed to load: {str(e)}")
                remove(f"{dirname}/{fp}")

    def outer_wrapper(func):
        def inner_wrapper(uri):
            try:
                return func.cache[uri]
            except KeyError:
                LOG.debug(f"Uncached URI: {uri}")
                func.cache[uri] = result = func(uri)
                fp = f"{JSON_CACHE}/{uri[1:].replace('/', '_')}.json"
                with open(fp, "w") as f:
                    f.write(json.dumps(result))
                return result

        return inner_wrapper

    return outer_wrapper(func)


def __SRD_API_CALL():
    """
    Closure for API calls
    """
    SRD_API = environ.get("SRD_API", "http://dnd5eapi.co")

    @cached_json
    def get_from_SRD(uri):
        import requests

        LOG.warning(f"Live API request! {str(uri)}")

        return requests.get(f"{SRD_API}{uri}").json()

    return get_from_SRD


SRD = __SRD_API_CALL()

SRD_endpoints = SRD("/api/")
SRD_classes = {}
SRD_class_levels = {}

for result in SRD(SRD_endpoints["classes"])["results"]:
    SRD_classes[result["index"]] = SRD(result["url"])
    SRD_class_levels[result["index"]] = SRD(result["url"] + "/levels")

SRD_rules = {
    category["name"]: {
        subsection["name"]: SRD(subsection["url"])["desc"]
        for subsection in SRD(category["url"])["subsections"]
    }
    for category in SRD(SRD_endpoints["rules"])["results"]
}
