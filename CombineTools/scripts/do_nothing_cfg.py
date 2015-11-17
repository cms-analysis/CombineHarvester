import FWCore.ParameterSet.Config as cms
process = cms.Process("MAIN")

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())

