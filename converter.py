import shapefile
from pygeoif import MultiPolygon


FILE = 'data/ne_10m_admin_1_states_provinces.shp'


def __print_properties(record: shapefile._Record):

    print(f"wikipediaid: {record.get('wikidataid')}")
    print(f"admin: {record.get('admin')}")
    print(f"iso_a2: {record.get('iso_a2')}")
    print(f"iso_3166_2: {record.get('iso_3166_2')}")
    print(f"adm1_code: {record.get('adm1_code')}")
    print(f"name: {record.get('name')}")
    print(f"name_ja: {record.get('name_ja')}")
    print(f"latitude: {record.get('latitude')}")
    print(f"longitude: {record.get('longitude')}")


def __shape_to_multipolygon(shape: shapefile.Shape) -> str:
    return MultiPolygon(shape).wkt


def main():
    with shapefile.Reader(FILE, encoding='utf-8') as reader:

        print(f"bbox: {reader.bbox}")
        print(f"num records: {reader.numRecords}")
        print()

        for shapeRecord in reader.iterShapeRecords():
            shape = shapeRecord.shape
            record = shapeRecord.record.as_dict()

            # for debug
            if not record["iso_3166_2"] == "JP-13":
                continue

            print(f"shape type: {shape.shapeTypeName}")
            __print_properties(record)
            print()

            print(__shape_to_multipolygon(shape))
            print()


if __name__ == '__main__':
    main()
