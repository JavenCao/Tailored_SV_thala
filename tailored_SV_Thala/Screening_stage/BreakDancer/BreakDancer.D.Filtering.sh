cd BD_pre
mkdir Raw_file
mv ./* ./Raw_file

mkdir QCed_Report
awk 'BEGIN{print "chr\tpos1\tpos2\tsize\tDeletion_with_support_Reads\tsample_name"}'  > ./QCed_Report/BreakDancer_Deletion.pre

cd ./Raw_file

for i in simu_{1491..1730} simu_{100..159}
do
	awk  -v Sname=$i '{if($7=="DEL" && $10 >= 4 && $8 >= 30){print $1"\t"$2"\t"$5"\t"$8"\t"$10"\t"Sname}}' BD_"$i".pre >> ../QCed_Report/BreakDancer_Deletion.pre
done

# find probably causal

cd ../QCed_Report

sort -k1,1 -k2,2n BreakDancer_Deletion.pre > mid_sorted_BreakDancer_Deletion.pre

bedtools closest -a mid_sorted_BreakDancer_Deletion.pre -b /paedwy/disk1/yjcao/datacenter/FinalSimu/100bp/SV/Screening_stage/Pindel/sorted.known_SV_Deletion_30bp.bed -d > BD_Causal.mid.bed

python Find_minimum_range.py --bed BD_Causal.mid.bed -minbed BD_Causal.pre

rm -rf BD_Causal.mid.bed mid_sorted_BreakDancer_Deletion.pre
