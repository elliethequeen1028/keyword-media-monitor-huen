from typing import Any, Dict

from strictyaml import Enum, Map, Seq, Str, Int, Bool, load


schema = Map({
    "targets": Seq(
        Map({
            "name": Str(),
            "base_url": Str(),
            "type": Enum(["news", "forum"]),
        })
    ),

    "keywords": Map({
        "primary": Seq(Str()),
        "secondary": Seq(Str()),
    }),

    "languages": Seq(Str()),

    "schedule": Map({
        "interval_minutes": Int(),
    }),

    "storage": Map({
        "type": Enum(["local"]),
        "path": Str(),
        "format": Enum(["json"]),
    }),

    "retention": Map({
        "cleanup_cycle_days": Int(),
    }),

    "alerts": Map({
        "enabled": Bool(),
        "method": Enum(["email"]),
    }),
})


def parse(configuration: str) -> Dict[str, Any]:
    return load(configuration, schema)
