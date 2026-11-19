from __future__ import annotations

import customtkinter as ctk


COULEURS = {
    "page": "#9E9E9E",
    "barre": "#4A4A4A",
    "onglet_actif": "#A6A6A6",
    "onglet_survol": "#5C5C5C",
    "cadre": "#D2D2D2",
    "panneau": "#FFFFFF",
    "bordure": "#1A1A1A",
    "bouton": "#FFFFFF",
    "bouton_survol": "#F0F0F0",
    "texte": "#111111",
    "texte_navigation": "#F2F2F2",
    "quitter": "#C00000",
}

ONGLETS = (
    ("livres", "Livres"),
    ("users", "Users"),
    ("sauvegarde", "Sauvegarde"),
)


class BarreNavigation(ctk.CTkFrame):
    def __init__(self, parent, commande, **kwargs):
        super().__init__(
            parent,
            fg_color=COULEURS["barre"],
            corner_radius=0,
            height=127,
            **kwargs,
        )
        self.grid_propagate(False)
        self.command = commande
        self.boutons = {}

        conteneur = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        conteneur.pack(side="bottom", anchor="w", padx=30)

        for cle, libelle in ONGLETS:
            bouton = ctk.CTkButton(
                conteneur,
                text=libelle,
                width=227,
                height=78,
                corner_radius=0,
                border_width=0,
                fg_color="transparent",
                hover_color=COULEURS["onglet_survol"],
                text_color=COULEURS["texte_navigation"],
                font=("Helvetica", 24),
                command=lambda nom=cle: self.command(nom),
            )
            bouton.pack(side="left", padx=(0, 16))
            self.boutons[cle] = bouton

    def set_actif(self, cle_active):
        for cle, bouton in self.boutons.items():
            actif = cle == cle_active
            bouton.configure(
                fg_color=COULEURS["onglet_actif"] if actif else "transparent",
                hover_color=COULEURS["onglet_actif"] if actif else COULEURS["onglet_survol"],
            )


class PagePrincipale(ctk.CTkFrame):
    def __init__(self, parent, commande_quitter, **kwargs):
        super().__init__(parent, fg_color=COULEURS["page"], corner_radius=0, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        cadre = ctk.CTkFrame(
            self,
            fg_color=COULEURS["cadre"],
            border_width=1,
            border_color=COULEURS["bordure"],
            corner_radius=0,
        )
        cadre.grid(row=0, column=0, sticky="nsew", padx=30, pady=24)
        cadre.grid_rowconfigure(0, weight=1)
        cadre.grid_columnconfigure(0, weight=1)
        cadre.grid_columnconfigure(1, minsize=200)

        self.panneau_contenu = ctk.CTkFrame(
            cadre,
            fg_color=COULEURS["panneau"],
            border_width=1,
            border_color=COULEURS["bordure"],
            corner_radius=0,
        )
        self.panneau_contenu.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(20, 16),
            pady=20,
        )

        self.panneau_actions = ctk.CTkFrame(
            cadre,
            fg_color="transparent",
            corner_radius=0,
        )
        self.panneau_actions.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 30),
            pady=20,
        )
        self.panneau_actions.grid_rowconfigure(0, weight=1)
        self.panneau_actions.grid_columnconfigure(0, weight=1)

        self.zone_actions = ctk.CTkFrame(
            self.panneau_actions,
            fg_color="transparent",
            corner_radius=0,
        )
        self.zone_actions.grid(row=0, column=0, sticky="new")

        self.bouton_quitter = ctk.CTkButton(
            self.panneau_actions,
            text="Quitter",
            width=150,
            height=44,
            corner_radius=8,
            border_width=1,
            border_color=COULEURS["bordure"],
            fg_color=COULEURS["bouton"],
            hover_color=COULEURS["bouton_survol"],
            text_color=COULEURS["quitter"],
            font=("Helvetica", 18),
            command=commande_quitter,
        )
        self.bouton_quitter.grid(row=1, column=0, sticky="e")


class PageLivres(PagePrincipale):
    pass


class PageUsers(PagePrincipale):
    pass


class PageSauvegarde(PagePrincipale):
    pass


class ApplicationBibliotheque(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("Bibliothèque")
        self.geometry("1120x840")
        self.minsize(900, 680)
        self.configure(fg_color=COULEURS["page"])

        self.grid_rowconfigure(0, minsize=127)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.navigation = BarreNavigation(self, self.afficher_page)
        self.navigation.grid(row=0, column=0, sticky="nsew")

        self.conteneur = ctk.CTkFrame(
            self,
            fg_color=COULEURS["page"],
            corner_radius=0,
        )
        self.conteneur.grid(row=1, column=0, sticky="nsew")
        self.conteneur.grid_rowconfigure(0, weight=1)
        self.conteneur.grid_columnconfigure(0, weight=1)

        self.pages = {
            "livres": PageLivres(self.conteneur, self.quitter),
            "users": PageUsers(self.conteneur, self.quitter),
            "sauvegarde": PageSauvegarde(self.conteneur, self.quitter),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

        self.afficher_page("livres")
        self.protocol("WM_DELETE_WINDOW", self.quitter)

    def afficher_page(self, cle):
        self.pages[cle].tkraise()
        self.navigation.set_actif(cle)

    def quitter(self):
        self.destroy()


if __name__ == "__main__":
    application = ApplicationBibliotheque()
    application.mainloop()
