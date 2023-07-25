"""
A cached function that gets SRD data from a DND 5e REST API
"""
import json
from os import environ, walk, path, remove, mkdir
import logging
from typing import Callable, TypeAlias, Union

LOG = logging.getLogger(__package__)
LOG.setLevel(logging.DEBUG)

try:
    JSON_CACHE = f"{path.dirname(path.abspath(__file__))}/json_cache"
    if not path.exists(JSON_CACHE):
        mkdir(JSON_CACHE)

except Exception as e:
    LOG.error(f"Entire JSON cache failed to load: {str(e)}")


# Json Data is unstructured and could be recursively nested
JsonValues: TypeAlias = Union[str, int, list["JsonValues"], dict[str, "JsonValues"]]
JsonData: TypeAlias = dict[str, JsonValues]


class DecoratedAPICallable:
    """
    Instantiated by the @cached_json decorator to wrap API calls.
    """

    def __init__(self, func: Callable[[str], JsonData]):
        self.func = func
        self.cache: dict[str, JsonData] = {}

    def __call__(self, uri: str) -> JsonData:
        return self.func(uri)


def cached_json(func: Callable[[str], JsonData]) -> Callable[[str], JsonData]:
    """
    This decorator returns a DecoratedAPICallable, which will return cached data
    if it exists. If it does not exist, then it will send a GET request to the API
    and try to save the response to a local JSON file to prevent future requests.
    """
    func = DecoratedAPICallable(func)
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

    def outer_wrapper(
        func: DecoratedAPICallable,
    ) -> Callable[[str], JsonData]:
        def inner_wrapper(uri: str) -> JsonData:
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


def __SRD_API_CALL() -> Callable[[str], JsonData]:
    """
    Closure for API calls
    """
    SRD_API = environ.get("SRD_API", "http://dnd5eapi.co")

    @cached_json
    def get_from_SRD(uri: str) -> JsonData:
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
