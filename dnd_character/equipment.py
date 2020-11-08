from .SRD import SRD_endpoints, SRD

SRD_equipment = {
    result["index"]: SRD(result["url"])
    for result in SRD(SRD_endpoints["equipment"])["results"]
}
