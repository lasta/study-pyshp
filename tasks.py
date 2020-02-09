import shapefile
import pygeoif
from typing import Iterable, Iterator, Dict
from csv import DictWriter
from invoke import task

GEOMETRY_FIELD_NAME = 'geometry'


def __read(
    shapefile_path: str,
    encoding: str = 'utf-8',
    debug: bool = False,
) -> Iterator[shapefile.ShapeRecord]:
    with shapefile.Reader(shapefile_path, encoding=encoding) as reader:
        if debug:
            print(f"bbox: {reader.bbox}")
            print(f"num records: {reader.numRecords}")
            print(list(field[0] for field in reader.fields))

        for shapeRecord in reader.iterShapeRecords():
            if debug:
                shape = shapeRecord.shape
                record = shapeRecord.record.as_dict()
                if not record["iso_a2"] == "JP":
                    continue
                print(record)
                print()
                print(f"shape type: {shape.shapeTypeName}")
                print(pygeoif.as_shape(shape).wkt)
            yield(shapeRecord)


def __apply_geometry_field(appendee: Dict, shape: shapefile.Shape):
    appendee[GEOMETRY_FIELD_NAME] = pygeoif.as_shape(shape).wkt
    return appendee


def __to_csv(
    shape_records: Iterable[shapefile.ShapeRecord],
    output: str,
    encoding='utf-8'
):
    first_element = next(shape_records)
    record = first_element.record.as_dict()
    fieldnames = list(record.keys())
    fieldnames.append(GEOMETRY_FIELD_NAME)

    with open(output, 'w', encoding=encoding) as output_file:
        writer = DictWriter(
            output_file,
            fieldnames=fieldnames,
            delimiter='\t'
        )
        writer.writeheader()

        shape = first_element.shape
        modified_record = __apply_geometry_field(record, shape)
        writer.writerow(modified_record)

        for shape_record in shape_records:
            record = shape_record.record.as_dict()
            shape = shape_record.shape
            modified_record = __apply_geometry_field(record, shape)
            writer.writerow(modified_record)


@task
def shp2csv(c, shape_file, csv_file, encoding='utf-8', debug=False):
    shapes = __read(shapefile_path=shape_file, encoding=encoding, debug=debug)
    __to_csv(shape_records=shapes, output=csv_file, encoding=encoding)
