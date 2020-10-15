from raspcuterie import base_path
from raspcuterie.devices.relay import manager
from raspcuterie.scripts.am2302 import append_file

relay_file = base_path / "relay.json"

if not relay_file.exists():
    relay_file.write_text("[]")

append_file(relay_file, manager.is_on(1))
