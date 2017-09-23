from .dependency import Dependency
from .ocurrence import Ocurrence
from .license import License

class Version(object):
	"""docstring for Version"""
	def __init__(self, ecosystemDataManager, package, index):
		super(Version, self).__init__()
		if not ecosystemDataManager or index == None:
			raise Exception
		self.ecosystemDataManager = ecosystemDataManager
		if not package:
			versionsHasPackage = self.ecosystemDataManager.get("VersionsHasPackage")
			package = self.ecosystemDataManager.getPackageByIndex(versionsHasPackage[index])
		self.package = package
		self.index = index

	def getIndex(self):
		return self.index

	def getPackage(self):
		return self.package

	def set(self, attribute, value):
		table = self.ecosystemDataManager.get(attribute)
		table[self.index] = value

	def get(self, attribute):
		table = self.ecosystemDataManager.get(attribute)
		return table[self.index]

	def getName(self):
		return self.get("VersionsHasIndex")

	def setDatetime(self, datetime):
		self.set("VersionsHasDatetime", datetime)
		return self

	def getDatetime(self):
		return self.get("VersionsHasDatetime")

	def setDownloads(self, downloads):
		self.set("VersionsHasDownloads", downloads)
		return self

	def getDownloads(self):
		return self.get("VersionsHasDownloads")

	def setLinesOfCode(self, linesOfCode):
		self.set("VersionsHasLinesOfCode", linesOfCode)
		return self

	def getLinesOfCode(self):
		return self.get("VersionsHasLinesOfCode")

	def getLocalRegularityRate(self):
		return self.get("VersionsHasLocalRegularityRate")

	def getGlobalRegularityRate(self):
		globalRegularityRate = self.get("VersionsHasGlobalRegularityRate")
		if not globalRegularityRate:
			globalRegularityRate = self.calculateGlobalRegularityRate()
			self.set("VersionsHasGlobalRegularityRate", globalRegularityRate)
		return globalRegularityRate

	def getLicenseByIndex(self, index):
		if index < 0:
			raise Exception
		try:
			return License(self.ecosystemDataManager, self, index)
		except Exception as e:
			raise e

	def addLicense(self, license):
		versionsHasLicenses = self.get("VersionsHasLicenses")
		licensesHasGroup = self.get("LicensesHasGroup")
		if license in versionsHasLicenses:
			licenseIndex = versionsHasLicenses.index(license)
		else:
			licenseIndex = len(versionsHasLicenses)
			licensesHasGroup.append(None)
			versionsHasLicenses.append(license)
		return self.getLicenseByIndex(licenseIndex)

	def setLicenses(self, licenses):
		self.set("VersionsHasLicenses", [])
		self.set("LicensesHasGroup", [])
		return [self.addLicense(license) for license in licenses]

	def getLicenses(self):
		versionsHasLicenses = self.get("VersionsHasLicenses")
		licenses = []
		for license in versionsHasLicenses:
			licenses.append(self.getLicenseByIndex(len(licenses)))
		return licenses

	def setAuthor(self, author):
		self.set("VersionsHasAuthor", author)
		return self

	def getAuthor(self):
		return self.get("VersionsHasAuthor")

	def setEmail(self, email):
		self.set("VersionsHasEmail", email)
		return self

	def getEmail(self):
		return self.get("VersionsHasEmail")

	def satisfies(self, strVersion):
		name = self.getName()
		for i in range(len(name)):
			if strVersion[i] == "x":
				return True
			elif strVersion[i] != name[i]:
				return False
		return True

	def addDependency(self, version):
		versionsHasDependencies = self.ecosystemDataManager.get("VersionsHasDependencies")
		if version.getIndex() in versionsHasDependencies[self.index]:
			dependencyIndex = versionsHasDependencies[self.index].index(version.getIndex())
		else:
			versionsHasOcurrences = self.ecosystemDataManager.get("VersionsHasOcurrences")
			dependenciesHasDelimiter = self.ecosystemDataManager.get("DependenciesHasDelimiter")
			dependenciesHasRequirements = self.ecosystemDataManager.get("DependenciesHasRequirements")
			dependenciesAreIrregular = self.ecosystemDataManager.get("DependenciesAreIrregular")

			dependencyIndex = len(versionsHasDependencies[self.index])
			versionsHasDependencies[self.index].append(version.getIndex())
			versionsHasOcurrences[version.getIndex()].append(self.getIndex())
			dependenciesHasDelimiter[self.index].append(None)
			dependenciesHasRequirements[self.index].append(None)
			dependenciesAreIrregular[self.index].append(None)
		packagesHasOcurrences = self.ecosystemDataManager.get("PackagesHasOcurrences")
		if self.package.getIndex() in packagesHasOcurrences[version.getPackage().getIndex()]:
			pass
		else:
			packagesHasOcurrences[version.getPackage().getIndex()].append(self.package.getIndex())
		return Dependency(self.ecosystemDataManager, self, version, dependencyIndex)

	def manageRecursion(self, start):
		if start:
			self.ecosystemDataManager.visited = []
		elif self in self.ecosystemDataManager.visited:
			return []
		else:
			self.ecosystemDataManager.visited.append(self)

	def getDependencies(self, recursive = False, start = True):
		self.manageRecursion(start)
		versionsHasDependencies =  self.ecosystemDataManager.get("VersionsHasDependencies")
		indexes = versionsHasDependencies[self.index]
		dependencies = []
		for dependency in indexes:
			inVersion = Version(self.ecosystemDataManager, None, dependency)
			dependencies.append(Dependency(self.ecosystemDataManager, self, inVersion, len(dependencies)))
		if recursive:
			descendents = []
			descendents += dependencies
			for dependency in dependencies:
				descendents += dependency.getInVersion().getDependencies(True, False)
			return descendents
		return dependencies

	def getOcurrences(self, recursive = False, start = True):
		self.manageRecursion(start)
		versionsHasOcurrences =  self.ecosystemDataManager.get("VersionsHasOcurrences")
		indexes = versionsHasOcurrences[self.index]
		ocurrences =  [Ocurrence(self, Version(self.ecosystemDataManager, None, ocurrence)) for ocurrence in indexes]
		if recursive:
			parents = []
			parents += ocurrences
			for ocurrence in ocurrences:
				parents += ocurrence.getInVersion().getOcurrences(True, False)
			return parents
		return ocurrences

	def getDescendents(self, start = True):
		self.manageRecursion(start)
		dependencies = self.getDependencies()
		descendents = []
		for dependency in dependencies:
			descendents.append(dependency.getInVersion())
			descendents += dependency.getInVersion().getDescendents(False)
		descendents = set(descendents)
		descendents = list(descendents)
		return descendents

	def getParents(self, start = True):
		self.manageRecursion(start)
		ocurrences = self.getOcurrences()
		parents = []
		for ocurrence in ocurrences:
			parents.append(ocurrence.getInVersion())
			parents += ocurrence.getInVersion().getParents(False)
		parents = set(parents)
		parents = list(parents)
		return parents

	def getContext(self):
		context = self.getParents() + self.getDescendents()
		context = set(context)
		context = list(context)
		return context

	def isIrregular(self):
		dependencies = self.getDependencies()
		for dependency in dependencies:
			if dependency.isIrregular():
				return True
		return False

	def isRegular(self):
		dependencies = self.getDependencies()
		for dependency in dependencies:
			if dependency.isIrregular():
				return False
		return True

	def getIrregularDependencies(self):
		return [dependency for dependency in self.getDependencies() if dependency.isIrregular()]

	def getRegularDependencies(self):
		dependencies = self.getDependencies()
		irregularDependencies = self.getIrregularDependencies()
		return list(set(dependencies) - set(irregularDependencies))

	def calculateLocalRegularityRate(self):
		try:
			localRegularityRate = len(self.getRegularDependencies()) / len(self.getDependencies())
		except Exception as e:
			localRegularityRate = 1
		self.set("VersionsHasLocalRegularityRate", localRegularityRate)
		return localRegularityRate

	def calculateGlobalRegularityRate(self):
		globalRegularityRate = self.getLocalRegularityRate()
		dependencies = self.getDependencies()
		for dependency in dependencies:
			globalRegularityRate *= dependency.getInVersion().getGlobalRegularityRate()
		self.set("VersionsHasGlobalRegularityRate", globalRegularityRate)
		return globalRegularityRate

	def __hash__(self):
		return self.index

	def __eq__(self, other):
		if type(other) != type(self):
			return False
		return other.getIndex() == self.getIndex()

	def __str__(self):
		return self.getPackage().getName() + "@" + str(self.getName())