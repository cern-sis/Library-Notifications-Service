import datetime

import pytest
from api import AnnualReportsAPI
from models import Categories, Journals, Publications
from sqlalchemy.orm import Session


class TestAPI:
    def setup_class(self):
        self.annual_reports = AnnualReportsAPI(
            years=[2022],
            db_user="annual",
            db_password="annual",
            db_host="localhost",
            db_port="5432",
            db_name="annual",
        )
        self.annual_reports.create_tables()

    @pytest.mark.vcr()
    def test_publications(self):
        with Session(self.annual_reports.engine) as session:
            publications = session.query(Publications).all()
            assert len(publications) == 0

        self.annual_reports.get_publications()

        with Session(self.annual_reports.engine) as session:
            publications = session.query(Publications).all()
            assert len(publications) == 1
            assert publications[0].publications == 2127
            assert publications[0].published_articles == 982
            assert publications[0].contributions_to_conference_proceedings == 1118
            assert publications[0].reports_books_and_book_chapters == 26
            assert publications[0].theses == 275
            assert publications[0].year == datetime.date(2022, 1, 1)

        with Session(self.annual_reports.engine) as session:
            session.query(Publications).delete()
            session.commit()

    @pytest.mark.vcr()
    def test_categories(self):
        with Session(self.annual_reports.engine) as session:
            categories = session.query(Categories).all()
            assert len(categories) == 0

        self.annual_reports.get_categories()

        with Session(self.annual_reports.engine) as session:
            categories = session.query(Categories).all()
            assert len(categories) == 19

            expected = {
                "Computing and Computers": 16,
                "Accelerators and Storage Rings": 38,
                "Astrophysics and Astronomy": 16,
                "Nuclear Physics - Experiment": 15,
                "Health Physics and Radiation Effects": 1,
                "Detectors and Experimental Techniques": 44,
                "Quantum Technology": 7,
                "Mathematical Physics and Mathematics": 5,
                "Education and Outreach": 3,
                "Physics in General": 6,
                "Particle Physics - Experiment": 18,
                "General Theoretical Physics": 2,
                "Other Fields of Physics": 3,
                "Particle Physics - Phenomenology": 22,
                "General Relativity and Cosmology": 6,
                "Particle Physics - Theory": 6,
                "Particle Physics - Lattice": 2,
                "Nuclear Physics - Theory": 6,
                "Engineering": 1,
            }
            for category in categories:
                assert category.category in expected
                assert category.count == expected[category.category]
                assert category.year == datetime.date(2022, 1, 1)

        with Session(self.annual_reports.engine) as session:
            session.query(Categories).delete()
            session.commit()

    @pytest.mark.vcr()
    def test_journals(self):
        with Session(self.annual_reports.engine) as session:
            journals = session.query(Journals).all()
            assert len(journals) == 0

        self.annual_reports.get_journals()

        with Session(self.annual_reports.engine) as session:
            journals = session.query(Journals).all()

            assert len(journals) == 117

            expected = {
                "JISTaP": 1,
                "IEEE Trans. Appl. Supercond.": 2,
                "The Messenger": 1,
                "IFAC-PapersOnLine": 1,
                "Future Microbiology": 1,
                "Frontiers in Medicine": 1,
                "J. Radiol. Prot.": 1,
                "EJNMMI Physics": 1,
                "Nature Chem.": 1,
                "Transport in Porous Media": 1,
                "IEEE Access": 3,
                "Materials": 1,
                "Environ. Sci. Technol.": 2,
                "IEEE Trans. Rad. Plasma Med. Sci.": 2,
                "CEAS Space J.": 1,
                "Environments": 1,
                "IEEE Trans. Parallel Distrib. Syst.": 2,
                "IEEE Systems J.": 1,
                "J. Chem. Phys.": 1,
                "J. Math. Industry": 1,
                "Inverse Prob. Imaging": 1,
                "Photon.": 2,
                "Chin. Phys. C": 1,
                "Polymers": 1,
                "J. Comput. Appl. Math.": 1,
                "Eur. Financ. Manag.": 1,
                "MagnetoHydrodyn.": 1,
                "Phys. Educ.": 1,
                "Atmos. Chem. Phys.": 1,
                "Phys. Status Solidi B": 1,
                "ACM Transactions on Privacy and Security": 1,
                "Comput. Phys. Commun.": 1,
                "Crystals": 5,
                "Acta Mater.": 1,
                "ChemPhysChem": 1,
                "Swiss Journal of Geosciences": 1,
                "Front. Phys.": 4,
                "Robotics": 1,
                "Nucl. Instrum. Methods Phys. Res., A": 12,
                "Phys. Rev. Accel. Beams": 9,
                "IEEE Trans. Educ.": 1,
                "J. Mach. Learn. Res.": 1,
                "J. Integer Sequences": 1,
                "Batteries": 1,
                "Comp. Meth. Appl. Math.": 1,
                "Pharmaceutics": 1,
                "Fortschr. Phys.": 1,
                "JHEP": 11,
                "IEEE Trans. Plasma Sci.": 1,
                "Phys. Part. Nucl. Lett.": 1,
                "Advanced Materials Interfaces": 1,
                "MDPI Physics": 2,
                "Phys. Rev. D": 6,
                "EPL": 1,
                "Phys. Rev. C": 5,
                "Appl. Opt.": 1,
                "Nature Astron.": 1,
                "JINST": 10,
                "AIP Adv.": 1,
                "JCAP": 1,
                "Res. Notes AAS": 1,
                "Appl. Sciences": 3,
                "J. Appl. Phys.": 1,
                "J. Phys. A": 1,
                "Eur. Phys. J. A": 1,
                "Astron. Astrophys.": 1,
                "Instruments": 1,
                "IEEE Trans. Quantum Eng.": 1,
                "Radiat. Prot. Dosim.": 1,
                "Bull. Russ. Acad. Sci. Phys.": 1,
                "IEEE Sensors J.": 1,
                "Int. J. Sci. Edu.": 1,
                "Fire Safety J.": 1,
                "Front. Chem.": 1,
                "Environmental Science: Atmospheres": 1,
                "Mach. Learn. Sci. Tech.": 2,
                "Roy. Soc. Open Sci.": 1,
                "EPJ Tech. Instrum.": 2,
                "Eur. Phys. J. Plus": 4,
                "J. Mater. Chem.": 1,
                "Front. Big Data": 1,
                "Sensors": 1,
                "The Physics Educator": 1,
                "Phys. Rev. B": 2,
                "J. Vac. Sci. Technol. A": 1,
                "Materials Advances": 1,
                "Sci. Rep.": 3,
                "PoS": 1,
                "Supercond. Sci. Technol.": 4,
                "Rev. Sci. Instrum.": 1,
                "Nature": 1,
                "Model. Simul. Eng.": 1,
                "Comput. Softw. Big Sci.": 1,
                "Appl. Radiat. Isot.": 2,
                "Phys. Lett. B": 2,
                "Phys. Rev. E": 2,
                "Swiss Medical Weekly": 1,
                "J. Radioanal. Nucl. Chem.": 1,
                "Nucl. Phys. News": 2,
                "Nature Commun.": 1,
                "PTEP": 1,
                "Phys. Rev. Res.": 1,
                "Nucl. Instrum. Methods Phys. Res., B": 2,
                "New J. Phys.": 1,
                "J. Lightwave Technol.": 1,
                "Opt. Lett.": 1,
                "Symmetry": 1,
                "Pramana - J. Phys.": 1,
                "Few-Body Syst.": 1,
                "IEEE Trans. Nucl. Sci.": 1,
                "Eur. Phys. J. C": 2,
                "J. Phys. D": 1,
                "Phys. Rev. Lett.": 3,
                "Astrophys. J. Lett.": 1,
                "Phys. Plasmas": 1,
                "IEEE Trans. Electron Devices": 1,
                "Rad. Det. Tech. Meth.": 1,
            }
            for journal in journals:
                assert journal.journal in expected
                assert journal.count == expected[journal.journal]
                assert journal.year == datetime.date(2022, 1, 1)

        with Session(self.annual_reports.engine) as session:
            session.query(Journals).delete()
            session.commit()
