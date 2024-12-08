class Stock:
    """
    Classe para manipulação e agregação de informações de estoque.
    """

    RISK_CATEGORIES = ['Critical', 'Low', 'Medium', 'High', 'Full']

    def __init__(self, data):
        """
        Inicializa o objeto com os dados de estoque.
        """
        self.data = data

    def filter_data(self, machine_id=None, product_name=None, quantity_category=None):
        """
        Filtra os dados de estoque com base nos parâmetros fornecidos.

        Parameters:
        ----------
        machine_id : str or None
            Filtra pelo ID da máquina.
        product_name : str or None
            Filtra pelo nome do produto.
        quantity_category : str or None
            Filtra pela categoria de quantidade.

        Returns:
        -------
        list:
            Dados filtrados.
        """
        filtered_data = self.data

        if machine_id:
            filtered_data = [row for row in filtered_data if row["machine_id"] == machine_id]

        if product_name:
            filtered_data = [row for row in filtered_data if row["product_name"] == product_name]

        if quantity_category:
            filtered_data = [row for row in filtered_data if row["quantity_category"] == quantity_category]

        return filtered_data

    def aggregate(self, granularity, operation):
        """
        Agrega os dados de estoque com base na granularidade e operação especificadas.

        Parameters:
        ----------
        granularity : str
            Nível de granularidade ("all", "no_machine", "no_product").
        operation : str
            Tipo de operação ("sum", "average", "count").

        Returns:
        -------
        list:
            Lista de dicionários com os dados agregados.
        """
        grouped_data = {}

        for row in self.data:
            if granularity == "no_machine":
                key = row["product_name"]
            elif granularity == "no_product":
                key = row["machine_id"]
            else:
                key = f"{row['machine_id']}-{row['product_name']}"

            if key not in grouped_data:
                grouped_data[key] = {
                    "machine_id": "Todos" if granularity == "no_machine" else row["machine_id"],
                    "product_name": "Todos" if granularity == "no_product" else row["product_name"],
                    "quantity": 0,
                    "count": 0,
                    "quantity_category": row["quantity_category"],
                    "location": row["location"]
                }

            # Atualiza a quantidade total e a contagem
            grouped_data[key]["quantity"] += row["quantity"]
            grouped_data[key]["count"] += 1

            # Mantém a categoria de maior risco
            current_category = grouped_data[key]["quantity_category"]
            new_category = row["quantity_category"]
            if Stock.RISK_CATEGORIES.index(new_category) < Stock.RISK_CATEGORIES.index(current_category):
                grouped_data[key]["quantity_category"] = new_category

        # Aplica a operação final
        for key, value in grouped_data.items():
            if operation == "average":
                value["quantity"] = value["quantity"] / value["count"]
            elif operation == "count":
                value["quantity"] = value["count"]

        # Deleta a contagem dos dados agregados
        for key in grouped_data:
            del grouped_data[key]["count"]

        return list(grouped_data.values())
