import csv
# from django.db import models
#
# class ProductParameters(models.Model):
#     id = models.AutoField(primary_key=True)
#     type = ProductParameterTypes.orm_field()
#     name = models.CharField(max_length=256)
#
# class ProductParameterLink(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     product = models.IntegerField()
#     parameter = models.IntegerField()
#     repair_price = models.DecimalField(decimal_places=2, max_digits=10)

class RepairPriceLoader:
    csv_delimiter = ';'
    parameter_column_name = 'ID детали'
    def __init__(self, price_file_path):
        self.price_file_path = price_file_path

    def create_parameters_dict(self):
        with open(self.price_file_path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.csv_delimiter)
            parameters_for_product = {}
            for row in reader:
                parameter_id = row.pop(self.parameter_column_name)
                parameters_for_product[parameter_id] = row
        return parameters_for_product

    def update_db_prices(self):
        parameters_dict = self.create_parameters_dict()
        for parameter_id, products in parameters_dict.items():
            for product, repair_price in products.items():
                try:
                    product_parameter_link = ProductParameterLink.objects.get(product=product, parameter=parameter_id)\
                        .update(repair_price=float(repair_price))
                except ProductParameterLink.DoesNotExist:
                    continue


l = RepairPriceLoader('price-commas.csv')
print(l.create_parameters_dict())
