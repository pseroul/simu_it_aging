
import pandas as pd
from datetime import datetime

class Server:

    def __init__(self,
                 manufacturing_cost: int,
                 power_consumption: int,
                 lifetime: int,
                 commissioning: int) -> None:
        """
        Create a server with the given args.
        Args: 
            manufacturing_cost (int): kgCO2e for the manufacturing
            power_consumption (int): Consumption in Watt
            lifetime (int) : Years of services
            commissioning (date): year of first use
        """
        self.manufacturing_cost = manufacturing_cost
        self.power_consumption = power_consumption
        self.lifetime = lifetime
        self.commissioning = commissioning
        self.decommissioning = self.commissioning + lifetime - 1

    def get_year_footprint(self, year: int, carbon_intensity: float) -> float:
        """
            Returns the server footprint for a given year.
            Args:
                year (int): the year of interest
                carbon_intensity (float): the quality of electricity used (kgCO2e/kWh)

            Returns: 
                float: Sum of manufacturing and usage cost
        """
        if year < self.commissioning or year > self.decommissioning:
            return 0
        manuf = self.manufacturing_cost / self.lifetime
        usage = self.power_consumption * 365 * 24 * carbon_intensity / 1000
        return manuf + usage


def build_servers_footprint(experience_years, manufacturing_cost, power_consumption, power_factor, lifetime, carbon_intensity):
    servers = []
    initial_year = datetime.now().year
    projection = initial_year

    while projection < initial_year + experience_years:
        power = power_consumption * power_factor.loc[projection, 'Energy perf comp 2023'] / power_factor.loc[initial_year, 'Energy perf comp 2023']
        server = Server(manufacturing_cost, power, lifetime, projection)
        servers.append(server)
        projection = server.decommissioning + 1
    
    years = [x for x in range(initial_year, initial_year + experience_years)]
    footprint = pd.DataFrame(index=years, columns = ['emissions (kgCO2e)', 'cumulated emissions (kgCO2e)'])
    for year in years:
        cumul = 0
        for server in servers:
            cumul += server.get_year_footprint(year, carbon_intensity)
        footprint.loc[year,'emissions (kgCO2e)'] = cumul
    
    footprint['cumulated emissions (kgCO2e)'] = footprint['emissions (kgCO2e)'].cumsum()
    return footprint