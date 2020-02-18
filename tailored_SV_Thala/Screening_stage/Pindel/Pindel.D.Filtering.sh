for chr in chr11 chr16
do
	cd /paedwy/disk1/yjcao/datacenter/FinalSimu/100bp/SV/Screening_stage/Pindel/P_pre/"$chr"
	mkdir Raw_file
	mv ./* Raw_file
	mkdir QCed_Report
	awk 'BEGIN{print "chr\tpos1\tpos2\tsize\tDeletion_with_support_Reads\tsample_name"}'  > ./QCed_Report/Pindel_Deletion.pre
	cd ./Raw_file

	# focusing on deletion only
	for i in simu_{1491..1730}
	do
		awk  '{if(/BP_range/ && ($11-$10 >100)){print}}' "$chr"_BD_Pindel_"$i"_D | awk -v Sname=$i '{if($16 >= 5){print $8"\t"$10"\t"$11"\t"$11-$10"\t"$16"\t"Sname}}' >> ../QCed_Report/Pindel_Deletion.pre
	done
	cd ../QCed_Report
done

# find exact mathed SVs
# find time to implement in python
awk 'BEGIN{FS=OFS="\t"}NR==FNR{a[$1"_"$2"_"$3]=$4"\t"$5}NR>FNR{if(a[$1"_"$2"_"$3]){print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"a[$1"_"$2"_"$3]}}' /paedwy/disk1/yjcao/datacenter/FinalSimu/100bp/SV/Screening_stage/Pindel/known_SV_Deletion_30bp.bed Pindel_Deletion.pre > Causal_Pindel_Deletion.pre
