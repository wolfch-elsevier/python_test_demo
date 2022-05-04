import json
import re
from collections import OrderedDict

from faker import Faker


class FakeNameAddressPhoneEmailStream:
    """Generate fake name, address, phone, email, records

    Needs: pip install faker

    Sample usage:
    fake_name_address_generator = FakeNameAddressPhoneEmail()

    for i, subscriber in enumerate(fake_name_address_generator.records()):
        pprint.pprint(subscriber)
        if i == 5:  # generate 5 sample records
            break

    TODO: put this into some shared, common test utility library
    """
    def __init__(self) -> None:
        self.fake = Faker()
        self.csz = re.compile(r"((?:\w+\s)*(?:\w+)),\s(\w\w)\s(\d\d\d\d\d)")

    def records(self) -> dict:
        while True:
            record = OrderedDict()
            record["name"] = self.fake.name()
            strt_city_st_zip = self.fake.address()
            parts = strt_city_st_zip.split('\n')
            address = OrderedDict()
            address["street"] = parts[0]
            m = self.csz.match(parts[1])
            if not m:  # Faker doesn't always generate a sensible "city, state" (sometimes no comma)
                # sys.stderr.write(f"Can't match csz: {parts[1]}\n")
                continue
            address["city"] = m.groups()[0]
            address["state"] = m.groups()[1]
            address["zip"] = m.groups()[2]
            record["address"] = address
            record["email"] = self.fake.email()
            record["home_phone"] = self.fake.phone_number()
            yield record  # use generator pattern for "infinite" stream of records


class JSONSerializer:
    def __init__(self, record_src, compact_fmt=True) -> None:
        pass


if __name__ == "__main__":
    fake_name_address_generator = FakeNameAddressPhoneEmailStream()
    records = []
    for i, record in enumerate(fake_name_address_generator.records()):
        record["serial"] = i
        # pprint(record)
        records.append(record)
        if i == 3:
            break
    # with open("fake_addresses.yaml", "w") as fh:
    #     yaml.dump(records, fh)
    print(json.dumps(records, sort_keys=False, indent=2))
