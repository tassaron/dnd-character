from .SRD import SRD_endpoints, SRD

SRD_monsters = {
    result["index"]: SRD(result["url"])
    for result in SRD(SRD_endpoints["monsters"])["results"]
}
