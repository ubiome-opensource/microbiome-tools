# uBiome tools
# by Richard Sprague
# GPL Public License

# first, set your working directory to the place you put the data:
# setwd(".") # you may want to change this line to a different directory.
#
# may<-read.csv("sprague-uBiomeMay2014.csv")
# jun<-read.csv("sprague-uBiomeJun2014.csv")

#data for June has weird headings, so this section makes the names consistent
# junNames<-names(jun)
# junNamesS<-strsplit(junNames,"\\.")
# names(junNamesS)<-NULL
# junNamesT<-sapply(junNamesS,function(x){x[2]})
# names(jun)<-junNamesT
#
# oct<-read.csv("sprague-uBiomeOct2014.csv")
# names(jun)
# names(oct)


# returns a dataframe showing how the two samples compare
# returns the count_norm of sample2 - sample1 (i.e. positive numbers indicate more in sample2)
uBiome_compare_samples <- function(sample1,sample2,rank="species"){

        #pull out just the rows made of the tax rank of interest (usually "species")
        s1Rank <-sample1[sample1$tax_rank==rank,]
        s2Rank <-sample2[sample2$tax_rank==rank,]

        # which tax_rank (e.g. species) from sample 1 are still found in sample 2?
        s1_still_found<-which(s1Rank$tax_name %in% s2Rank$tax_name)
        s2_still_found<-which(s2Rank$tax_name %in% s1Rank$tax_name)

        s1_table<-s1Rank[s1_still_found,] # full table of all sample 1 species still found in sample 2
        s2_table<-s2Rank[s2_still_found,]
        #handy: note that rownames(s2_table) maintains references to the original row names from sample2

        s1_tA<-s1_table[order(s1_table$tax_name),] #alphabetized version of s1_table
        s2_tA<-s2_table[order(s2_table$tax_name),] #alphabetized version of s2_table

        # Return a new data frame with proper column headings
        change_s1_s2 <-data.frame(s1_tA$tax_name,s2_tA$count_norm - s1_tA$count_norm)#, row.names=c("tax_name","count_change"))
        names(change_s1_s2)=c("tax_name","count_change")
        change_s1_s2
}

# which tax rank items (e.g. species) are found in sample1 but not sample2?
uBiome_sample_unique <- function (sample1,sample2,rank="species"){

        #pull out just the rows made of the tax rank of interest (usually "species")
        s1Rank <-sample1[sample1$tax_rank==rank,]
        s2Rank <-sample2[sample2$tax_rank==rank,]

        inS1NotS2<-! (s1Rank$tax_name %in% s2Rank$tax_name)
        s1_not <- which(inS1NotS2 )
        missing <-s1Rank[s1_not,]
        missing <- missing[order(missing$count_norm,decreasing=TRUE),] #sort the result by count_norm (normalized count)
        data.frame(missing$count_norm,missing$tax_name)

}
