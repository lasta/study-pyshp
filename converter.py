import shapefile

FILE = 'data/ne_10m_admin_1_states_provinces.shp'


def main():
    src = shapefile.Reader(FILE, encoding='utf-8')

    print(src.bbox)
    print(src.numRecords)

    for shapeRecord in src.iterShapeRecords():
        shape = shapeRecord.shape
        record = shapeRecord.record

        print(shape)
        for element in record:
            print(element)

        return


if __name__ == '__main__':
    main()
