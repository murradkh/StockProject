pipeline {
agent any
    parameters {
     choice(name: "Version", choices: ['1.0','1.2','1.3'], description: '')
     booleanParam(name:'executeTests', defaultValue: true, description: '')
    }
stages{
stage("build"){
    when {
        expression {
         params.executeTests == true   
        }
    }
steps {
echo "building the application"
}

}
stage("test"){
steps{
echo "testing the application"
    echo "testing ${params.Version}"
}
}
stage("deploy"){
steps{
echo "deploying the application"
}

}

}
}
