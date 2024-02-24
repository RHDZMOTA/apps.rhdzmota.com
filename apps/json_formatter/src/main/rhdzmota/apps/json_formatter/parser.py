import uuid
import json
import ast
import logging
import textwrap
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union


@dataclass(frozen=True, slots=True)
class JSONParserOutput:
    payload: Optional[dict] = None

    def flatten(self, include_lists: bool = False) -> Optional[dict]:
        # Early exit if None, [], or {}
        if not self.payload:
            return self.payload

        def recursive(payload: Union[dict, list]) -> dict:
            if isinstance(payload, list):
                return payload if not include_lists else recursive(
                    payload={str(i): item for i, item in enumerate(payload)}
                )
            return {
                (f"{og_key}.{in_key}" if in_key else og_key): in_val
                for og_key, og_val in payload.items()
                for in_key, in_val in (
                    recursive(og_val).items()
                    if isinstance(og_val, dict) or isinstance(og_val, list) 
                    else [(None, og_val)]
                )
            }

        return recursive(payload=self.payload)

    @property
    def ok(self) -> bool:
        return isinstance(self.payload, dict) or isinstance(self.payload, list)


@dataclass(frozen=True, slots=True)
class JSONParser:
    string: str
    use_single_quotes: bool = False

    @property
    def uuid(self) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_OID, self.string))

    def parse(self, fail: bool = False, **kwargs) -> JSONParserOutput:
        try:
            return JSONParserOutput(
                payload=ast.literal_eval(self.string, **kwargs)
                    if self.use_single_quotes else json.loads(self.string, **kwargs)
                )
        except Exception as e:
            if fail:
                raise
            # TODO: Add logger
            return JSONParserOutput()
