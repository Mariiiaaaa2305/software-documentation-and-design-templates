using MyLab.Domain;

namespace MyLab.DataAccessLayer;

public interface IUserRepository
{

    List<User> ReadUsersFromCsv(string filePath);

    void SaveUsersToDatabase(List<User> users);
}
