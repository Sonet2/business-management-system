class WoodCatalog:
    def __init__(self, connection):
        self.connection = connection


    def _fetch_flat_list(self, query, params=()):
        rows = self.connection.execute(query,params).fetchall()
        return[row[0] for row in rows]
    
    def get_wood_category(self) -> list:
        results = self._fetch_flat_list("SELECT DISTINCT category FROM materials")
        return results
    
    def get_wood_subcategory(self,category):
        results = self._fetch_flat_list("SELECT DISTINCT subcategory FROM materials WHERE category = ?",(category,))

        if results == [None]:
            return None
        return results
            
        
    def get_wood_specie(self, category, subcategory):
        if subcategory is None:
            check_query = "SELECT DISTINCT wood_species_id FROM materials WHERE category = ? AND subcategory IS NULL"
            check_params = (category,)
        else:
            check_query = "SELECT DISTINCT wood_species_id FROM materials WHERE category = ? AND subcategory = ?"
            check_params = (category, subcategory)

        ids = self._fetch_flat_list(check_query, check_params)

        if ids == [None]:
            return None
        if not ids:
            return []

        if subcategory is None:
            query = (
                "SELECT DISTINCT wood_species.name FROM materials "
                "INNER JOIN wood_species ON materials.wood_species_id = wood_species.id "
                "WHERE category = ? AND subcategory IS NULL"
            )
            params = (category,)
        else:
            query = (
                "SELECT DISTINCT wood_species.name FROM materials "
                "INNER JOIN wood_species ON materials.wood_species_id = wood_species.id "
                "WHERE category = ? AND subcategory = ?"
            )
            params = (category, subcategory)
        return self._fetch_flat_list(query, params)
        
    def get_wood_price(self, category, subcategory, wood_specie):
        conditions = ["materials.category = ?"]
        params = [category]

        if subcategory is None:
            conditions.append("materials.subcategory IS NULL")
        else:
            conditions.append("materials.subcategory = ?")
            params.append(subcategory)

        if wood_specie is None:
            conditions.append("materials.wood_species_id IS NULL")
        else:
            conditions.append("wood_species.name = ?")
            params.append(wood_specie)

        query = (
            "SELECT price_per_m3_grosze FROM materials "
            "LEFT JOIN wood_species ON materials.wood_species_id = wood_species.id "
            "WHERE " + " AND ".join(conditions)
        )
        return self._fetch_flat_list(query, tuple(params))