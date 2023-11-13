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
            cds_token="haha",
        )

    @pytest.fixture(autouse=True)
    def setup_tests(self):
        self.annual_reports.drop_tables()
        self.annual_reports.create_tables()
        yield
        self.annual_reports.drop_tables()

    @pytest.mark.vcr()
    def test_publications(self):
        self.annual_reports.get_publications()

        with Session(self.annual_reports.engine) as session:
            publications = session.query(Publications).all()
            assert len(publications) == 1
            assert publications[0].publications == 2123
            assert publications[0].journals == 978
            assert publications[0].contributions == 1117
            assert publications[0].rest == 27
            assert publications[0].theses == 278
            assert publications[0].year == datetime.date(2022, 1, 1)

    @pytest.mark.vcr()
    def test_subjects(self):
        self.annual_reports.get_subjects()

        with Session(self.annual_reports.engine) as session:
            categories = session.query(Categories).all()
            assert len(categories) == 23

            expected = {
                "Particle Physics - Experiment": 357,
                "Particle Physics - Phenomenology": 255,
                "Detectors and Experimental Techniques": 156,
                "Nuclear Physics - Experiment": 115,
                "Particle Physics - Theory": 114,
                "Accelerators and Storage Rings": 113,
                "Astrophysics and Astronomy": 96,
                "General Relativity and Cosmology": 60,
                "Computing and Computers": 41,
                "Nuclear Physics - Theory": 39,
                "Other Fields of Physics": 27,
                "Health Physics and Radiation Effects": 23,
                "Particle Physics - Lattice": 17,
                "Mathematical Physics and Mathematics": 15,
                "Physics in General": 15,
                "General Theoretical Physics": 13,
                "Quantum Technology": 9,
                "Engineering": 8,
                "Chemical Physics and Chemistry": 6,
                "Condensed Matter": 6,
                "Education and Outreach": 6,
                "Nonlinear Systems": 3,
                "Other Subjects": 1,
            }
            for category in categories:
                assert category.category in expected
                assert category.count == expected[category.category]
                assert category.year == datetime.date(2022, 1, 1)

    @pytest.mark.vcr()
    def test_journals(self):
        self.annual_reports.get_publications()

        with Session(self.annual_reports.engine) as session:
            journals = session.query(Journals).all()

            assert len(journals) == 193

            expected = {
                "JHEP": 173,
                "Phys. Rev. D": 100,
                "Eur. Phys. J. C": 71,
                "Phys. Rev. Lett.": 50,
                "Phys. Lett. B": 44,
                "JINST": 41,
                "Nucl. Instrum. Methods Phys. Res., A": 40,
                "Phys. Rev. Accel. Beams": 25,
                "Eur. Phys. J. Plus": 23,
                "Phys. Rev. C": 20,
                "IEEE Trans. Nucl. Sci.": 19,
                "JCAP": 15,
                "Front. Phys.": 13,
                "Nature": 10,
                "SciPost Phys.": 9,
                "Comput. Softw. Big Sci.": 8,
                "Eur. Phys. J. A": 7,
                "Mach. Learn. Sci. Tech.": 7,
                "Sci. Rep.": 7,
                "Appl. Sciences": 6,
                "Crystals": 6,
                "EPJ Tech. Instrum.": 6,
                "IEEE Trans. Appl. Supercond.": 6,
                "Nature Phys.": 6,
                "Supercond. Sci. Technol.": 6,
                "Symmetry": 6,
                "Front. Big Data": 5,
                "Phys. Rev. B": 5,
                "Rep. Prog. Phys.": 5,
                "Rev. Sci. Instrum.": 5,
                "Sensors": 5,
                "Ann. Phys. (Leipzig)": 4,
                "Astron. Astrophys.": 4,
                "Nucl. Instrum. Methods Phys. Res., B": 4,
                "Appl. Phys. Lett.": 3,
                "Appl. Radiat. Isot.": 3,
                "Comput. Phys. Commun.": 3,
                "Cryogenics": 3,
                "Fortschr. Phys.": 3,
                "IEEE Access": 3,
                "Instruments": 3,
                "Int. J. Mod. Phys. A": 3,
                "J. Phys. A": 3,
                "J. Phys. G": 3,
                "MDPI Physics": 3,
                "Mon. Not. R. Astron. Soc.": 3,
                "Nature Commun.": 3,
                "New J. Phys.": 3,
                "Nucl. Phys. News": 3,
                "Phys. Rev. A": 3,
                "Prog. Part. Nucl. Phys.": 3,
                "Quantum": 3,
                "Universe": 3,
                "Astropart. Phys.": 2,
                "Class. Quantum Gravity": 2,
                "Environ. Sci. Technol.": 2,
                "EPL": 2,
                "IEEE Sensors J.": 2,
                "IEEE Trans. Parallel Distrib. Syst.": 2,
                "IEEE Trans. Rad. Plasma Med. Sci.": 2,
                "Int. J. Heat Mass Transf.": 2,
                "Nucl. Phys. B": 2,
                "Photon.": 2,
                "Phys. Dark Univ.": 2,
                "Phys. Educ.": 2,
                "Phys. Med. Biol.": 2,
                "Phys. Rev. E": 2,
                "Phys. Rev. Res.": 2,
                "PTEP": 2,
                "SciPost Phys. Proc.": 2,
                "ACM Trans. Reconf. Tech. Syst.": 1,
                "ACM Transactions on Privacy and Security": 1,
                "ACS Earth Space Chem.": 1,
                "Acta Mater.": 1,
                "Advanced Materials Interfaces": 1,
                "Advances in Radiation Oncology": 1,
                "AIP Adv.": 1,
                "Anal. Chim. Acta": 1,
                "Ann. Rev. Nucl. Part. Sci.": 1,
                "Appl. Opt.": 1,
                "Astrophys. J. Lett.": 1,
                "Atmos. Chem. Phys.": 1,
                "Batteries": 1,
                "Bull. Russ. Acad. Sci. Phys.": 1,
                "CEAS Space J.": 1,
                "ChemPhysChem": 1,
                "Chin. Phys. C": 1,
                "Clinical and Translational Radiation Oncology": 1,
                "Commun. Math. Phys.": 1,
                "Comp. Meth. Appl. Math.": 1,
                "Data in Brief": 1,
                "EJNMMI Physics": 1,
                "Environmental Science: Atmospheres": 1,
                "Environments": 1,
                "Eur. Financ. Manag.": 1,
                "Eur. J. Phys.": 1,
                "Eur. Phys. J.": 1,
                "Eur. Phys. J. D": 1,
                "Eur. Phys. J. Spec. Top.": 1,
                "Experimental Thermal and Fluid Science": 1,
                "Few-Body Syst.": 1,
                "Fire Safety J.": 1,
                "Front. Chem.": 1,
                "Frontiers in Medicine": 1,
                "Future Gener. Comput. Syst.": 1,
                "Future Microbiology": 1,
                "Geochim. Cosmochim. Acta": 1,
                "Heliyon": 1,
                "IEEE Systems J.": 1,
                "IEEE Trans. Educ.": 1,
                "IEEE Trans. Electron Devices": 1,
                "IEEE Trans. Microw. Theory Tech.": 1,
                "IEEE Trans. Plasma Sci.": 1,
                "IEEE Trans. Quantum Eng.": 1,
                "IFAC-PapersOnLine": 1,
                "Int. J. Heat Fluid FL": 1,
                "Int. J. Sci. Edu.": 1,
                "Int. J. Theor. Phys.": 1,
                "Interface Focus": 1,
                "Inverse Prob. Imaging": 1,
                "J. Appl. Phys.": 1,
                "J. Chem. Phys.": 1,
                "J. Comput. Appl. Math.": 1,
                "J. Integer Sequences": 1,
                "J. Lightwave Technol.": 1,
                "J. Mach. Learn. Res.": 1,
                "J. Mater. Chem.": 1,
                "J. Mater. Process Tech.": 1,
                "J. Math. Industry": 1,
                "J. Phys. B": 1,
                "J. Phys. D": 1,
                "J. Phys.: Conf. Ser.": 1,
                "J. Radioanal. Nucl. Chem.": 1,
                "J. Radiol. Prot.": 1,
                "J. Res. Sci. Teach.": 1,
                "J. Stat. Phys.": 1,
                "J. Vac. Sci. Technol. A": 1,
                "JHEAp": 1,
                "JISTaP": 1,
                "Living Rev. Relativ.": 1,
                "MagnetoHydrodyn.": 1,
                "Materials": 1,
                "Materials Advances": 1,
                "Meas. Sci. Technol.": 1,
                "Metrolog.": 1,
                "Microelectron. Eng.": 1,
                "Microelectron. Reliab.": 1,
                "Mod. Phys. Lett. A": 1,
                "Model. Simul. Eng.": 1,
                "Nature Astron.": 1,
                "Nature Chem.": 1,
                "Nature Mach. Intell.": 1,
                "Nature Rev. Phys.": 1,
                "Nuovo Cimento, Riv.": 1,
                "Opt. Lett.": 1,
                "Optica": 1,
                "Optical Materials Express": 1,
                "Particles": 1,
                "Pharmaceutics": 1,
                "Philos. Trans. R. Soc. Lond. A": 1,
                "Phys. Part. Nucl.": 1,
                "Phys. Part. Nucl. Lett.": 1,
                "Phys. Plasmas": 1,
                "Phys. Rep.": 1,
                "Phys. Status Solidi B": 1,
                "Physica Medica": 1,
                "Physics": 1,
                "Polymers": 1,
                "PoS": 1,
                "Pramana - J. Phys.": 1,
                "Rad. Det. Tech. Meth.": 1,
                "Radiat. Meas.": 1,
                "Radiat. Phys. Chem.": 1,
                "Radiat. Prot. Dosim.": 1,
                "Radiother. Oncol.": 1,
                "Res. Notes AAS": 1,
                "Research Outreach": 1,
                "Robotics": 1,
                "Roy. Soc. Open Sci.": 1,
                "Sci. Adv.": 1,
                "Sci. Bull.": 1,
                "Sci. Data": 1,
                "Science": 1,
                "Smart Mater. Struct.": 1,
                "SN Comput. Sci.": 1,
                "Softw Pract Exper.": 1,
                "Surf. Coat. Technol.": 1,
                "Swiss Journal of Geosciences": 1,
                "Swiss Medical Weekly": 1,
                "The Messenger": 1,
                "The Physics Educator": 1,
                "Transport in Porous Media": 1,
                "Vacuum": 1,
            }

            for journal in journals:
                assert journal.journal in expected
                assert journal.count == expected[journal.journal]
                assert journal.year == datetime.date(2022, 1, 1)
