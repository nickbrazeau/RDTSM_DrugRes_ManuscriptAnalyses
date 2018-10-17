#!/usr/bin/python3
###############################################################################
# Purpose:  SnakeMake File to run SeekDeep for mali clearance analysis
# Authors: Nick Brazeau                                        
#Given: FASTQ
#Return: seekdeep 
###############################################################################

####### Working Directory and Project Specifics ############
#WRKDIR = '/proj/ideel/meshnick/users/NickB/Projects/EPHI_AmpliconResCollab/'
workdir: '/proj/ideel/meshnick/users/NickB/Projects/uganda_elevation_drugRx_Boyce'

# Run the second directory once the analysis dir is made

GENOMEDIR='/proj/ideel/resources/genomes/Pfalciparum/genomes'


rule all:
#    input: 'elucidator_Prep_report.txt'
    input: 'seekdeep_report.txt'
#    input: 'analysis/analysis_report.txt'

rule runanalysis:
    input: 'analysis/runAnalysis.sh'
    output: 'analysis/analysis_report.txt'
    shell: 'bash {input} --numThreads 7 ; \
    echo "seekdeep analysis complete" > output'

rule rundseekdeep:
    input: symlinks='symlinks', id='ids.txt', samplenames='sampleNames.tab.txt'
    output: 'seekdeep_report.txt'
    shell: 'SeekDeep setupTarAmpAnalysis --samples {input.samplenames} \
    --outDir analysis --inputDir {input.symlinks}/ --byIndex \
    --idFile {input.id} --lenCutOffs targetRefSeqs/forSeekDeep/lenCutOffs.txt \
    --overlapStatusFnp targetRefSeqs/forSeekDeep/overlapStatuses.txt \
    --refSeqsDir targetRefSeqs/forSeekDeep/refSeqs/ \
    --extraExtractorCmds="--barcodeErrors 1 --checkShortenBars --checkRevComplementForMids --checkRevComplementForPrimers" \
    --extraProcessClusterCmds="--illumina --fracCutOff 0.05" \
    ; echo "seekdeep run complete" > {output}'

rule extractor: 
    input: id='ids.txt'
    output: 'elucidator_Prep_report.txt'
    shell: 'elucidator genTargetInfoFromGenomes --primers {input.id} \
    --genomeDir {GENOMEDIR} --dout targetRefSeqs \
     --selectedGenomes Pf3d7,Pf7G8,PfDd2,PfGB4,PfHB3,PfIT \
     --pairedEndLength 300 --overWriteDir ; echo "elucidator setup worked" > {output}'
     
# http://baileylab.umassmed.edu/SeekDeep/illumina_paired_info.html
# need to account for the fact that ligation will put illumina adaptor on both sides so the MID and primer may have 3'-5' and/or 5'-3' orientation
