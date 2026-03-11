using Microsoft.EntityFrameworkCore;
using MyLab.Domain;

namespace MyLab.DataAccessLayer;

public class AppDbContext : DbContext
{
    public DbSet<User> Users { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        // База даних буде створена в головній папці під назвою mylab2.db
        optionsBuilder.UseSqlite("Data Source=../mylab2.db");
    }
}