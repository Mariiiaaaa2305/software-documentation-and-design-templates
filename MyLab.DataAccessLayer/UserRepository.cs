using MyLab.Domain;
using Microsoft.EntityFrameworkCore;

namespace MyLab.DataAccessLayer;

public class UserRepository : IUserRepository
{
    public List<User> ReadUsersFromCsv(string filePath)
    {
        var users = new List<User>();
        if (!File.Exists(filePath)) return users;

        var lines = File.ReadAllLines(filePath);
        foreach (var line in lines.Skip(1))
        {
            var parts = line.Split(',');
            if (parts.Length == 3)
            {
                users.Add(new User { 
                    Id = int.Parse(parts[0]), 
                    Name = parts[1], 
                    Email = parts[2] 
                });
            } 
        }
        return users;
    }

    public void SaveUsersToDatabase(List<User> users)
    {
        using var db = new AppDbContext();
        db.Database.EnsureCreated();
        

        db.Users.ExecuteDelete(); 
        
        db.Users.AddRange(users);
        db.SaveChanges();
        Console.WriteLine($"[DAL] Збережено {users.Count} юзерів у SQLite.");
    }
}
