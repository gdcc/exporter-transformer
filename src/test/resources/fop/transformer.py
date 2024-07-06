from java.io import ByteArrayInputStream, ByteArrayOutputStream, File
from java.lang import System
from java.util import Base64
from javax.xml.transform import TransformerFactory
from javax.xml.transform.sax import SAXResult
from javax.xml.transform.stream import StreamSource
from org.apache.fop.apps import FopFactory, MimeConstants

localeEnvVar = System.getenv().get("LANG") if System.getenv().get("LANG") else "en"
if localeEnvVar.index(".") > 0:
    localeEnvVar = localeEnvVar[0 : localeEnvVar.index(".")]
if localeEnvVar.index("_") > 0:
    localeEnvVar = localeEnvVar[0 : localeEnvVar.index("_")]

fopFactory = FopFactory.newInstance(File(".").toURI())
foUserAgent = fopFactory.newFOUserAgent()
out = ByteArrayOutputStream()
fop = fopFactory.newFop(MimeConstants.MIME_PDF, foUserAgent, out)

factory = TransformerFactory.newInstance()
factory.setURIResolver(
    lambda href, base: StreamSource(File(path + "/xslt/" + href))
)
transformer = factory.newTransformer(StreamSource(File(path + "/xslt/ddi-to-fo.xsl")))
transformer.setParameter("language-code", localeEnvVar)
src = StreamSource(ByteArrayInputStream(Base64.getDecoder().decode(x["base64"])))
saxRes = SAXResult(fop.getDefaultHandler())

transformer.transform(src, saxRes)

res["base64"] = Base64.getEncoder().encodeToString(out.toByteArray())
