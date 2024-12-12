library(doParallel)
library(phytools)


checker<-function(file,output){
    load(file)
    if ((typeof(model.ard)==typeof(list())) & ((typeof(model.er)==typeof(list())))){
        if (model.ard$loglik>model.er$loglik){
            tmatrix<-as.Qmatrix(model.ard)
            likmatrix<-model.ard$lik.anc
            model<-'ard'
            
        } else{
            tmatrix<-as.Qmatrix(model.er)
            likmatrix<-model.er$lik.anc
            model<-'er'

        }
    } else{
        if (typeof(model.ard)==typeof(list())) {
            tmatrix<-as.Qmatrix(model.ard)
            likmatrix<-model.er$lik.anc
            model<-'ard'

        } else{
            if (typeof(model.er)==typeof(list())){
            tmatrix<-as.Qmatrix(model.er)
            likmatrix<-model.er$lik.anc
            model<-'er'
            }
        }
    }
    fname<-basename(file)
    fname<-unlist(strsplit(fname,'\\.'))[1]
    write.table(tmatrix,file=paste(output,fname,'_transtion.tsv',sep=''),sep='\t',quote = F)
    write.table(likmatrix,file=paste(output,fname,'_likanc.tsv',sep=''),sep='\t',quote = F)
    return(data.frame(model = model, file = fname))
}

path_i='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/Ancestral_State_Reconstruction/16S_rRNA/asrFiles'
files<-list.files(path_i,full.names = T)
cl <- makeCluster(60)
registerDoParallel(cl)
result<-foreach(i=files,.packages = c('phytools','ape'),.export = c('checker')) %dopar%{
    output="/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/Ancestral_State_Reconstruction/16S_rRNA/asr_matrixes/"
    checker(i,output)
    
}
final_result <- do.call(rbind, result)
# print(unlist(result))

write.table(final_result, '/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/Ancestral_State_Reconstruction/16S_rRNA/model_og.tsv', sep = '\t', quote = FALSE)

stopCluster(cl)