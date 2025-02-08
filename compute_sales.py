import json
import sys
import time


def load_json(file_path):
    """Carga un archivo JSON y maneja errores."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar {file_path}: {e}")
        return None


def compute_sales(price_catalogue, sales_record):
    """Calcula el total de ventas basado en el catálogo de precios."""
    total_sales = 0.0
    errors = []

    # Convertir catálogo en un diccionario de títulos de productos a precios
    price_dict = {item["title"]: item["price"] for item in price_catalogue}

    for sale in sales_record:
        item = sale.get("Product")
        quantity = sale.get("Quantity")

        if item not in price_dict:
            errors.append(f"Producto no encontrado en catálogo: {item}")
            continue

        if not isinstance(quantity, (int, float)) or quantity < 0:
            errors.append(f"Cantidad inválida para {item}: {quantity}")
            continue

        total_sales += price_dict[item] * quantity

    return total_sales, errors


def main():
    """Función principal del programa."""
    if len(sys.argv) != 3:
        print("Uso: python computeSales.py priceCatalogue salesRecord")
        return

    price_file, sales_file = sys.argv[1], sys.argv[2]

    price_catalogue = load_json(price_file)
    sales_record = load_json(sales_file)

    if price_catalogue is None or sales_record is None:
        return

    start_time = time.time()
    total_sales, errors = compute_sales(price_catalogue, sales_record)
    elapsed_time = time.time() - start_time

    result_text = (
        f"Total de ventas: {total_sales:.2f}\n"
        f"Tiempo de ejecución: {elapsed_time:.4f} segundos"
    )

    if errors:
        result_text += "\n\nErrores encontrados:\n" + "\n".join(errors) + "\n"

    print(result_text)

    with open("SalesResults.txt", "w", encoding="utf-8") as result_file:
        result_file.write(result_text)


if __name__ == "__main__":
    main()
