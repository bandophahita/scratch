import re

ss = "(self, provider: Union[ForwardRef('BaseProvider'), Type[ForwardRef('BaseProvider')]]) -> None"

sig_str  = re.sub(r"ForwardRef\('([^']*)'\)", r"'\1'", ss)
sig_str2 = re.sub(r"ForwardRef\('([^']*)'\)", r"\1", ss)




expected_result = "(self, provider: Union['BaseProvider', Type['BaseProvider']]) -> None"


