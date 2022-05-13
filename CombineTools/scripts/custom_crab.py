from __future__ import print_function
def custom_crab(config):
    print('>> Customising the crab config')
    config.User.voGroup = 'dcms'
    config.Site.storageSite = 'T2_DE_DESY'
    config.Site.blacklist = ['T2_FI_HIP', 'T1_ES_PIC', 'T1_UK_RAL', 'T2_FR_CCIN2P3', 'T2_US_Nebraska', 'T1_IT_CNAF', 'T2_US_Vanderbilt']
    # config.JobType.maxMemoryMB = 4500
