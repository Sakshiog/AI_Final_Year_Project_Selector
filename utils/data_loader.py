import pandas as pd


class DataLoader:

    def __init__(self, project_path):
        self.project_path = project_path

    def load_projects(self):
        """Load project dataset."""
        return pd.read_csv(self.project_path)

    def get_domains(self):
        """Get unique project domains."""
        projects = self.load_projects()
        return sorted(projects["domain"].dropna().unique())

    def get_difficulties(self):
        """Get unique difficulty levels."""
        projects = self.load_projects()
        return sorted(projects["difficulty"].dropna().unique())


if __name__ == "__main__":

    loader = DataLoader("../data/projects.csv")

    projects = loader.load_projects()

    print("\nProject Dataset")
    print("================")

    print(f"Total Projects: {len(projects)}")

    print("\nAvailable Domains:")
    for domain in loader.get_domains():
        print("-", domain)

    print("\nDifficulty Levels:")
    for difficulty in loader.get_difficulties():
        print("-", difficulty)