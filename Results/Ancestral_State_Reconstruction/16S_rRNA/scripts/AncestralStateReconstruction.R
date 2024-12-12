#!/home/aswin/irsingh/softwares/miniconda3/envs/codingEnv/bin/Rscript
library(doParallel)
library(ape)
library(phytools)

asr <- function(dataFrame, treeFile, sep, output) {
    # Read data
    if (sep == 'c') {
        df <- read.csv(dataFrame, row.names = 1, sep = ',')
    } else {
        df <- read.csv(dataFrame, row.names = 1, sep = '\t')
    }
    print('dataFrameRead')

    # Read and preprocess tree
    tree <- read.tree(treeFile)
    tree <- phytools::midpoint.root(tree)
    tree <- multi2di(tree)
    tree$edge.length[tree$edge.length == 0] <- 1e-5
    tree$node.label <- NULL
    print('treeRead')
    df<-df[tree$tip.label,]
    # Parallel processing
    cl <- makeCluster(100)
    registerDoParallel(cl)
    colNames <- colnames(df)
    print('parel')
    foreach(i = colNames, .packages = c('ape', 'phytools')) %dopar% {
        cat("Processing column:", i, "\n")
        vector<-df[[i]]
        names(vector)<-row.names(df)
        model.er <- ace(vector, phy = tree, type = 'discrete', marginal = TRUE, model = "ER")
        model.ard <- ace(vector, phy = tree, type = 'discrete', marginal = TRUE, model = "ARD")
        imageName <- paste(output, i, 'asr', sep = '_')
        imageName <- paste(imageName, 'RData', sep = '.')
        save(model.er,model.ard,file = imageName)

    }
    stopCluster(cl)
}

dataFrame="/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/organismMatrix/hmmscanEG/binaryCount/eggNOG_hmmscan_ZnBROG_binary.tsv"

treeFile="/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/treeMaking/16s_GTDB/tree/16SrRNA_tree.besttree"

output="/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/Ancestral_State_Reconstruction/16S_rRNA/asrFiles/"

sep="t"

asr(dataFrame = dataFrame,treeFile = treeFile,sep=sep,output = output)