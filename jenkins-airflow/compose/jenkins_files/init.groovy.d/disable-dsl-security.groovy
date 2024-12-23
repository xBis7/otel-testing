import jenkins.model.*
import javaposse.jobdsl.plugin.GlobalJobDslSecurityConfiguration

// Disable script security for Job DSL
println("Disabling Job DSL Script Security...")

def instance = Jenkins.getInstance()
def globalDslSecurityConfig = instance.getDescriptorByType(GlobalJobDslSecurityConfiguration.class)
globalDslSecurityConfig.setUseScriptSecurity(false)

println("Job DSL Script Security has been disabled.")
