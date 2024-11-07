#include <stdio.h>
struct process
{
    int pid;
    int bt;
    int wt;
    int tat;
}p[20];
int main (){
    int i,n;
    struct process temp;
    float awt=0,atat=0;
    printf("Enter the no:of process:");
    scanf("%d",&n);
    printf("/n Enter the burst time:");
    for(i=0;i<n;i++){
        p[i].pid=i+1;
        printf("p[%d]:",p[i].pid);
        scanf("%d",&p[i].bt);
    }
    p[0].wt=0;
    p[0].tat=p[0].bt;
    atat=p[0].tat;
    for(i=1;i<n;i++){
        p[i-1].bt+p[i-1].wt;
        p[i].tat=p[i].bt+p[i].wt;
        awt=awt+p[i].wt;
        atat=atat+p[i].tat;
    }
    printf("\nprocess\t burst time \t waiting time \t turnaround time ");
    for(i=0;i<n;i++)
    printf("\n%d\t\t\t%d\t\t\t%d\t\t\t\t%d",p[i].pid,p[i].bt,p[i].wt,p[i].tat);
    }
    printf("\nGantt chart:\n");
    for(i=0;i<n;i++)
    printf("|%d   ",p[i].pid);
    printf("\n%d   ",0);
    for(i=0;i<n;i++)
    printf("%d    ",p[i].tat);
    printf("\n\naverage waiting time=%f",awt/n);
    printf("\naverage turnaroundtime=%f",awt/n);
    return 0;
    }