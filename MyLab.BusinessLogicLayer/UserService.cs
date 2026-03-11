using MyLab.DataAccessLayer;

namespace MyLab.BusinessLogicLayer;

public class UserService : IUserService
{
    private readonly IUserRepository _repo;

    public UserService(IUserRepository repo)
    {
        _repo = repo;
    }

    public void RunMigration(string csvPath)
    {
        Console.WriteLine("[BLL] Початок міграції даних...");
        var users = _repo.ReadUsersFromCsv(csvPath);
        _repo.SaveUsersToDatabase(users);
        Console.WriteLine("[BLL] Дані успішно перенесені в базу!");
    }
}