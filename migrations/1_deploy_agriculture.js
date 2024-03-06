const agriculture=artifacts.require('agriculture');

module.exports=function(deployer){
    deployer.deploy(agriculture);
}