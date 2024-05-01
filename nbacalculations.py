import sqlite3
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('complete.db')
cur = conn.cursor()

def get_salary_avg(cur):
    cur.execute("SELECT AVG(salary) FROM players")
    avg = cur.fetchone()[0] 
    return avg

def get_weight_avg(cur):
    cur.execute("SELECT AVG(weight) FROM players")
    avg_weight = cur.fetchone()[0]
    return avg_weight

def get_height_avg(cur):
    cur.execute("SELECT AVG(height) FROM players")
    avg_height = cur.fetchone()[0]
    return avg_height

def get_avg_experience(cur):
    cur.execute("SELECT AVG(experience) FROM players")
    avg_experience = cur.fetchone()[0]
    return avg_experience

def get_avg_dco(cur):
    cur.execute("SELECT AVG(depthchartorder) FROM players")
    avg_dco = cur.fetchone()[0]
    return avg_dco

# def get_sal_exp_corr(cur):
#     cur.execute("SELECT salary, experience FROM players  WHERE experience IS NOT NULL")
#     data = cur.fetchall()

#     salary = []
#     experience = []
#     for row in data:

#         salary.append(row[0])
#         experience.append(row[1])

#     corr_coef = np.corrcoef(salary, experience)[0, 1]
#     return corr_coef
def get_sal_exp_corr(cur):
    cur.execute("SELECT salary, experience FROM players")
    data = cur.fetchall()
    valid_data = [(row[0], row[1]) for row in data if all(row)]
    salary, experience = zip(*valid_data)
    if salary and experience:
        corr_coef = np.corrcoef(salary, experience)[0, 1]
        return corr_coef
    else:
        return None  


def exp_vs_sal(cur):
    cur.execute("SELECT experience, salary FROM players WHERE experience IS NOT NULL AND salary IS NOT NULL")
    data = cur.fetchall()
    experience = []
    salary = []
    for row in data:
        experience.append(row[0])
        salary.append(row[1])
    avg_experience = get_avg_experience(cur)
    slope, intercept = np.polyfit(experience, salary, 1)
    regression_line = [slope * x + intercept for x in experience]
    plt.scatter(experience, salary, color='pink', label= 'Data')
    plt.plot(experience, regression_line, color='magenta', label='Regression Line')
    plt.title('Average Experience vs Salary')
    plt.xlabel('Experience')
    plt.ylabel('Salary')
    plt.show()

def dco_vs_exp(cur):
    cur.execute("SELECT depthchartorder, experience FROM players WHERE depthchartorder IS NOT NULL AND experience IS NOT NULL")
    data = cur.fetchall()
    dco = []
    exp = []
    for row in data:
        dco.append(row[0])
        exp.append(row[1])
    

    plt.bar(dco, exp, color='purple')
    plt.title('Depth Chart Order vs Experience')
    plt.xlabel('Depth Chart Order')
    plt.ylabel('Experience')
 
  
    plt.show()

def writecalcs(cur):
    with open('calculated_data.txt', 'a') as file:
        file.write("Average Salary: {:.2f}\n".format(get_salary_avg(cur)))
        file.write("Average Weight: {:.2f}\n".format(get_weight_avg(cur)))
        file.write("Average Height: {:.2f}\n".format(get_height_avg(cur)))
        file.write("Average Experience: {:.2f}\n".format(get_avg_experience(cur)))
        file.write("Average Depth Chart Order: {:.2f}\n".format(get_avg_dco(cur)))
        file.write("Correlation between Salary and Experience: {:.2f}\n".format(get_sal_exp_corr(cur)))
        file.write("\n")

def main():
    cur = conn.cursor()
    
   
    
    exp_vs_sal(cur)
    dco_vs_exp(cur)

    writecalcs(cur)

    cur.close()
    conn.close()

   
if __name__ == "__main__":
    main()